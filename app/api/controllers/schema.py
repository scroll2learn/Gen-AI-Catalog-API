from typing import List, Optional
from urllib.parse import parse_qs

from app.core.config import Config
from app.utils.auth_wrapper import authorize
from app.utils.git_utils.git_wrapper import GitWrapper
from fastapi import APIRouter, Depends, Query, Request
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.enums.flow import SchemaTypes
from app.models.base import StatusMessage
from app.models.schema import Schema, SchemaCreate, SchemaReturn, SchemaUpdate
import json

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[SchemaReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_schemas(
    *,
    schema_id: Optional[int] = None,
    schema_type: Optional[str] = None,
    commit_id: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'schema_id', 'schema_type'"),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.schema_service.list(
        schema_id=schema_id,
        schema_type=schema_type,
        commit_id=commit_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search",
    response_model=List[SchemaReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_schema_fields(
    *,
    params: Optional[str] = Query(None, description="Search fields, e.g., schema_type=FLOW&commit_id=abc123"),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.schema_service.search(params=params)


@router.get(
    "/{schema_id}",
    response_model=SchemaReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_schema_by_id(
    *,
    schema_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.schema_service.get(id=schema_id)


@router.post(
    "",
    response_model=SchemaReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_schema(
    *,
    obj: SchemaCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.schema_service.create(obj=obj, authorized=authorized)


@router.put(
    "/{schema_id}",
    response_model=SchemaReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_schema(
    *,
    schema_id: int,
    obj: SchemaUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.schema_service.update(id=schema_id, obj=obj, authorized=authorized)


@router.delete(
    "/{schema_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_schema_by_id(
    schema_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    status = await ctx.schema_service.delete(id=schema_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}

@router.get(
    "/latest/{schema_type}",
    response_model=SchemaReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_latest_schema(
    *,
    schema_type: SchemaTypes,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    schema_id =  await ctx.schema_service.get_latest_by_type(schema_type=schema_type)

    return await ctx.schema_service.get(id=schema_id)

@router.get(
    "/get-schema-by-version-tag/{version_tag}",
    status_code=http_status.HTTP_200_OK,
)
async def get_schema_by_version_tag(
    *,
    version_tag: str,
    schema_type:SchemaTypes,
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    token = Config.TOKEN
    owner = Config.OWNER
    repo = Config.REPO
    git_provider = GitWrapper(token, owner, repo, 4100)
    if SchemaTypes.PIPELINE.value == schema_type.value:
        file_path = "pipeline/pipeline.json"
    elif SchemaTypes.FLOW.value == schema_type.value:
        file_path = "flows/flows.json"
    else:
        return {"status": 400, "message": "Invalid schema type."}
    result = await git_provider.get_file_content_by_version_tag(file_path=file_path, ref=version_tag)
    if result["status"] == 200:
        json_content = json.loads(result["content"])  
        return json.dumps(json_content, indent=4)
    else:
        return result['message']
    

@router.get(
    "/get-schema-version-tags-list/",
    status_code=http_status.HTTP_200_OK,
)
async def get_repo_branc_list(
    *,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    token = Config.TOKEN
    owner = Config.OWNER
    repo = Config.REPO
    git_provider = GitWrapper(token, owner, repo, 4100)
    result = await git_provider.get_tags()
    if result["status"] == 200:
        return {"tags": result}
    else:
        return result['message']
