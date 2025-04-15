import json
import re
from random import choices
from string import ascii_lowercase, digits
from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.enums.bh_project import Status
from app.exceptions import BHProjectAlreadyExists
from app.exceptions.bh_project import (BHProjectDoesNotExist,
                                       DecryptExceptionError)
from app.exceptions.gcp import BHSecretCreateError
from app.exceptions.git import (GitCreateBranchException,
                                GitRepoMismatchException, GitTokenNotValid,
                                GitUrlNotValid, GitUsernameNotAuthorized,
                                GitUsernameNotValid, GitWrapperException,
                                RepoDoesNotExistException)
from app.models.base import StatusMessage
from app.models.bh_project import (BHProjectCreate, BHProjectReturn,
                                   BHProjectUpdate, TokenValidationRequest)
from app.services.aes import decrypt_string, encrypt_string
from app.utils.auth_wrapper import authorize
from app.utils.constants import GITHUB_TOKEN
from app.utils.git_utils.git_utils import (check_git_url_format,
                                           extract_github_org_and_repo,
                                           extract_secret_name)
from app.utils.git_utils.git_wrapper import GitWrapper

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[BHProjectReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_bighammer_projects(
    *,
    bh_project_id: Optional[int] = None,
    bh_project_name: Optional[str] = None,
    bh_github_username: Optional[str] = None,
    status: Optional[Status] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'bh_project_cld_id', 'bh_project_name'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.bh_project_service.list(
        bh_project_id=bh_project_id,
        bh_project_name=bh_project_name,
        bh_github_username=bh_github_username,
        status=status,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[BHProjectReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, bh_project_name=abc&business_url=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.bh_project_service.search(params=params)


@router.get(
    "/{bh_project_id}",
    response_model=BHProjectReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_bighammer_project(
    *,
    bh_project_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    response = await ctx.bh_project_service.get(id=bh_project_id)
    secret_name = extract_secret_name(
        response.bh_github_token_url
    )  # Extract the secret name from the secret path
    secret_token = await ctx.gcp_service.secrets.get_secret(
        secret_name
    )  # Get the secret token from the secret manager
    encrypt_token, init_vector = encrypt_string(secret_token)  # Encrypt the string
    response.bh_github_token_url = encrypt_token
    return response


@router.post(
    "",
    response_model=BHProjectReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_bighammer_project(
    *,
    obj: BHProjectCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    project_exist = await ctx.bh_project_service.check_project_exists(
        obj.bh_project_name
    )
    if project_exist:
        raise BHProjectAlreadyExists(context={"name": obj.bh_project_name})
    github_org, repo = extract_github_org_and_repo(obj.bh_github_url)
    # Decrypt token
    try:
        obj.bh_github_token_url = decrypt_string(
            obj.bh_github_token_url, obj.init_vector
        )
    except Exception as e:
        raise DecryptExceptionError(context={"error": str(e)})
    
    try:
        git_provider = GitWrapper(
            obj.bh_github_token_url, github_org, repo, obj.bh_github_provider
        )
    except Exception as e:
        raise GitWrapperException(context={"error": str(e)})

    # Create branch
    response = await git_provider.create_branch(obj.bh_default_branch)
    if response.get("status") != 201:
        raise GitCreateBranchException(context={"error": str(response.get("message"))})
    try:
        formatted_name = obj.bh_project_name.replace(" ", "_").lower()
        secret_name = f"github_{formatted_name}_secret"
        # Storing token on aws secret manager
        secret_data = json.dumps({GITHUB_TOKEN: obj.bh_github_token_url})
        secret, version = await ctx.aws_service.secrets.new_secret(
            secret_name, secret_data
        )
        # Updating token with secret url
        obj.bh_github_token_url = version

    except Exception as e:
        raise BHSecretCreateError(
            context={"error": str(e), "name": obj.bh_project_name}
        )

    return await ctx.bh_project_service.create(obj=obj, authorized=authorized)


@router.put(
    "/{bh_project_id}",
    response_model=BHProjectReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_by_bighammer_project_id(
    *,
    bh_project_id: int,
    obj: BHProjectUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    return await ctx.bh_project_service.update(id=bh_project_id, obj=obj, authorized=authorized)


@router.delete(
    "/{bh_project_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_bighammer_project_by_id(
    bh_project_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.bh_project_service.delete(id=bh_project_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}


@router.post("/validate-token/")
async def validate_token(
    request: TokenValidationRequest,
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    try:
        github_org, repo = extract_github_org_and_repo(request.bh_github_url)
        request.bh_github_token_url = decrypt_string(
            request.bh_github_token_url, request.init_vector
        )
        git_provider = GitWrapper(
            token=request.bh_github_token_url,
            repo_owner=github_org,
            repo_name=repo,
            provider_type=request.bh_github_provider,
        )
    except Exception as e:
        raise GitWrapperException(context={"error": str(e)})

    # Call the validate_token method
    response = await git_provider.validate_token()
    if response.get("status") != 200:
        raise GitTokenNotValid()

    url = request.bh_github_url
    # Check the URL is in correct format
    check_git_url_format(url)

    # check repo exists for the org
    res = await git_provider.check_repo_exists()
    if res.get("status") != 200:
        raise RepoDoesNotExistException()
    response = await git_provider.validate_username(request.bh_github_username)
    if response.get("status") != 200:
        raise GitUsernameNotAuthorized()
    return {"status": http_status.HTTP_200_OK, "message": "Git Credentials Validated"}
