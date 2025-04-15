import json
import logging
from typing import List, Optional
from urllib.parse import parse_qs

from app.exceptions.aws import AWSSecretsClientError, MwaaEnvironmentNotFoundError
from app.models.aws import AWSCredentials
from app.services.aws import AWSMWAAService
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, HTTPException
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.enums.bh_project import Status
from app.enums.env import FlowConnectionType
from app.exceptions.bh_project import (DecryptExceptionError)
from app.exceptions.bh_project_env import BHProjectEnvDataInvalidError
from app.exceptions.gcp import BHSecretCreateError
from app.models.base import StatusMessage
from app.models.bh_project import (ConfigureLifecycleCreate,
                                   ConfigureLifecycleReturn,
                                   ConfigureLifecycleUpdate,
                                   FlowConnectionCreate, FlowConnectionReturn,
                                   FlowConnectionUpdate, LakeZoneCreate,
                                   LakeZoneReturn, LakeZoneUpdate,
                                   PreConfigureZoneCreate,
                                   PreConfigureZoneResponse,
                                   PreConfigureZoneReturn,
                                   PreConfigureZoneUpdate,
                                   ProjectEnvironmentCreate,
                                   ProjectEnvironmentReturn,
                                   ProjectEnvironmentUpdate)
from app.services.aes import decrypt_string
from app.utils.auth_wrapper import authorize
from app.utils.aws_utils import get_aws_encrypted_keys
from app.utils.cloud_service_utils import (check_json_file_type,
                                           get_secret_manager_formatted_name)
from app.utils.constants import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from app.utils.lake_zone_utils import generate_random_string
from app.utils.normalization import normalise_name
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/lake_zone/list/",
    response_model=List[LakeZoneReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_lake_zones(
    *,
    lake_zone_id: Optional[int] = None,
    lake_name: Optional[str] = None,
    business_url: Optional[str] = None,
    bh_env_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'lake_zone_name', 'lake_zone_desc'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.lake_zone_service.list(
        lake_zone_id=lake_zone_id,
        lake_name=lake_name,
        business_url=business_url,
        bh_env_id=bh_env_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/lake_zone/search",
    response_model=List[LakeZoneReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_lake_zone_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, lake_zone_name=abc&lake_zone_url=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.lake_zone_service.search(params=params)


@router.get(
    "/lake_zone/{lake_zone_id}",
    response_model=LakeZoneReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_lake_zone(
    *, lake_zone_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.lake_zone_service.get(id=lake_zone_id)


@router.post(
    "/lake_zone",
    response_model=PreConfigureZoneResponse,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_lake_zone(
    *, obj: LakeZoneCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):

    env = await ctx.project_environment_service.get(id=obj.bh_env_id)
    env_provider = await ctx.codes_dtl_service.get(id=env.bh_env_provider)
    env_cd = env_provider.dtl_desc[:1].lower() if env_provider else ""

    lake_zone = await ctx.lake_zone_service.create(obj=obj, authorized=authorized)
    lake_name = normalise_name(lake_zone.lake_name)

    zone_types = [
        "bronze_zone",
        "silver_zone",
        "gold_zone",
        "log_zone",
        "quarantine_zone",
    ]
    zone_map = {
        zone: f"s3://{lake_name}.{env_cd}.{zone[0]}.{generate_random_string()}.{lake_zone.business_url}"
        for zone in zone_types
    }

    return zone_map


@router.put(
    "/lake_zone/{lake_zone_id}",
    response_model=LakeZoneReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_lake_zone_by_id(
    *, lake_zone_id: int, obj: LakeZoneUpdate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.lake_zone_service.update(id=lake_zone_id, obj=obj, authorized=authorized)


@router.delete(
    "/lake_zone/{lake_zone_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_lake_zone_by_id(
    lake_zone_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.lake_zone_service.delete(id=lake_zone_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/environment/list/",
    response_model=List[ProjectEnvironmentReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_environment(
    *,
    bh_env_id: Optional[int] = None,
    bh_env_name: Optional[str] = None,
    airflow_url: Optional[str] = None,
    airflow_bucket_name: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'bh_env_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.project_environment_service.list(
        bh_env_id=bh_env_id,
        bh_env_name=bh_env_name,
        airflow_url=airflow_url,
        airflow_bucket_name=airflow_bucket_name,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/environment/search",
    response_model=List[ProjectEnvironmentReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_environment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, bh_env_name=abc&bh_env_provider=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.project_environment_service.search(params=params)


@router.get(
    "/environment/{project_environment_id}",
    response_model=ProjectEnvironmentReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_environment(
    *, project_environment_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    response = await ctx.project_environment_service.get_env(id=project_environment_id)
    if response.cloud_provider_cd == 101:
        secret_name = get_secret_manager_formatted_name(response.bh_env_name)
        aws_secret = await ctx.aws_service.secrets.get_secret(secret_name)
        access_key, secret_access_key = get_aws_encrypted_keys(aws_secret)
        response.access_key = access_key
        response.secret_access_key = secret_access_key
    return response


@router.post(
    "/environment",
    response_model=ProjectEnvironmentReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_environment(
    *,
    bh_env_name: str = Form(...),
    bh_env_provider: int = Form(...),
    cloud_provider_cd: int = Form(...),
    cloud_region_cd: int = Form(...),
    location: str = Form(None),
    tags: str = Form(None),
    project_id: str = Form(...),
    file: UploadFile = File(None),
    access_key: str = Form(None),
    secret_access_key: str = Form(None),
    airflow_url: str = Form(None),
    airflow_bucket_name: str = Form(None),
    airflow_env_name: str = Form(None),
    pvt_key: str = Form(None),
    init_vector: str = Form(None),
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    if access_key and secret_access_key:
        try:
            access_key = decrypt_string(access_key, init_vector)
            secret_access_key = decrypt_string(secret_access_key, init_vector)
        except Exception as e:
            raise DecryptExceptionError(context={"error": str(e)})

    #TODO will remove later
    # try:
    #     secret_name = get_secret_manager_formatted_name(bh_env_name)
    #     if cloud_provider_cd == 101:
    #         # Storing access and secret access key on secret manager AWS
    #         secret_data = json.dumps(
    #             {AWS_ACCESS_KEY: access_key, AWS_SECRET_ACCESS_KEY: secret_access_key}
    #         )
    #         secret, version = await ctx.aws_service.secrets.new_secret(
    #             secret_name, secret_data
    #         )

    #     elif cloud_provider_cd == 102:
    #         # Storing file content on secret manager GCP
    #         if file:
    #             # Check if file type is JSON
    #             check_json_file_type(file)

    #         file_content = await file.read()  # Read the file content
    #         secret, version = await ctx.gcp_service.secrets.new_secret(
    #             secret_name, file_content.decode()
    #         )

    # except Exception as e:
    #     raise BHSecretCreateError(context={"error": str(e), "name": bh_env_name})

    try:
        obj_data = {
            "bh_env_name": bh_env_name,
            "bh_env_provider": bh_env_provider,
            "cloud_provider_cd": cloud_provider_cd,
            "cloud_region_cd": cloud_region_cd,
            "location": location,
            "pvt_key": pvt_key,  # Updating pvt key with secret URL
            "status_cd": Status.ACTIVE.value,
            "tags": (
                json.loads(tags) if tags else None
            ),  # Convert from JSON string to dict
            "project_id": project_id,
            "airflow_url": airflow_url,
            "airflow_bucket_name": airflow_bucket_name,
            "airflow_env_name": airflow_env_name,
        }

        # Convert the dictionary to a ProjectEnvironmentCreate object
        obj = ProjectEnvironmentCreate(**obj_data)

    except Exception as e:
        raise BHProjectEnvDataInvalidError(context={"error": str(e)})

    return await ctx.project_environment_service.create(obj=obj, authorized=authorized)


@router.put(
    "/environment/{project_environment_id}",
    response_model=ProjectEnvironmentReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_environment_by_id(
    *,
    project_environment_id: int,
    obj: ProjectEnvironmentUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.project_environment_service.update(
        id=project_environment_id, obj=obj, authorized=authorized
    )


@router.delete(
    "/environment/{project_environment_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_environment_by_id(
    project_environment_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.project_environment_service.delete(id=project_environment_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/preconfigure-zone/list/",
    response_model=List[PreConfigureZoneReturn],
    status_code=http_status.HTTP_200_OK,
)
async def list_preconfigure_zone(
    *,
    pre_configure_id: int = None,
    bh_env_id: int = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'bh_env_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.pre_configure_zone_service.list(
        pre_configure_id=pre_configure_id,
        bh_env_id=bh_env_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/preconfigure-zone/{preconfigure_zone_id}",
    response_model=PreConfigureZoneReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_preconfigure_zone_by_id(
    *, preconfigure_zone_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.pre_configure_zone_service.get(id=preconfigure_zone_id)


@router.post(
    "/preconfigure-zone/",
    response_model=PreConfigureZoneReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def preconfigure_zone(
    *, obj: PreConfigureZoneCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.pre_configure_zone_service.create(obj=obj, authorized=authorized)


@router.put(
    "/preconfigure-zone/{preconfigure_zone_id}",
    response_model=PreConfigureZoneReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_preconfigure_zone_by_id(
    *,
    preconfigure_zone_id: int,
    obj: PreConfigureZoneUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.pre_configure_zone_service.update(id=preconfigure_zone_id, obj=obj, authorized=authorized)


@router.delete(
    "/preconfigure-zone/{preconfigure_zone_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_preconfigure_zone_by_id(
    preconfigure_zone_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.pre_configure_zone_service.delete(id=preconfigure_zone_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/configure-lifecycle/list/",
    response_model=List[ConfigureLifecycleReturn],
    status_code=http_status.HTTP_200_OK,
)
async def list_configure_lifecycle(
    *,
    configure_lifecycle_id: int = None,
    bh_env_id: int = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'bh_env_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.configure_lifecycle_service.list(
        configure_lifecycle_id=configure_lifecycle_id,
        bh_env_id=bh_env_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/configure-lifecycle/{configure_lifecycle_id}",
    response_model=ConfigureLifecycleReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_configure_lifecycle_by_id(
    *, configure_lifecycle_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.configure_lifecycle_service.get(id=configure_lifecycle_id)


@router.post(
    "/configure-lifecycle/",
    response_model=ConfigureLifecycleReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def configure_lifecycle(
    *, obj: ConfigureLifecycleCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.configure_lifecycle_service.create(obj=obj, authorized=authorized)


@router.put(
    "/configure-lifecycle/{configure_lifecycle_id}",
    response_model=ConfigureLifecycleReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_configure_lifecycle_by_id(
    *,
    configure_lifecycle_id: int,
    obj: ConfigureLifecycleUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.configure_lifecycle_service.update(
        id=configure_lifecycle_id, obj=obj, authorized=authorized
    )


@router.delete(
    "/configure-lifecycle/{configure_lifecycle_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_configure_lifecycle_by_id(
    configure_lifecycle_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.configure_lifecycle_service.delete(id=configure_lifecycle_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/flow-connection/list/",
    response_model=List[FlowConnectionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def list_flow_connection(
    *,
    id: int = None,
    connection_id: str = None,
    connection_type: FlowConnectionType = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'bh_env_name'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.flow_connection_service.list(
        id=id,
        connection_id=connection_id,
        connection_type=connection_type,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/flow-connection/{flow_connection_id}",
    response_model=FlowConnectionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_connection_by_id(
    *, flow_connection_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.flow_connection_service.get(id=flow_connection_id)


@router.post(
    "/flow-connection/",
    response_model=FlowConnectionReturn,
    status_code=http_status.HTTP_201_CREATED,
    description="Connection Name should be lowercase and with underscore",
)
async def flow_connection(
    *, obj: FlowConnectionCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.flow_connection_service.create(obj=obj, authorized=authorized)


@router.put(
    "/flow-connection/{flow_connection_id}",
    response_model=FlowConnectionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_connection_by_id(
    *,
    flow_connection_id: int,
    obj: FlowConnectionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    return await ctx.flow_connection_service.update(id=flow_connection_id, obj=obj, authorized=authorized)


@router.delete(
    "/flow-connection/{flow_connection_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_connection_by_id(
    flow_connection_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.flow_connection_service.delete(id=flow_connection_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/connections/{bh_env_id}/http_connections", status_code=http_status.HTTP_200_OK
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)

    # TODO will change this later
    return [
        "http_connection_1",
        "http_connection_2",
        "http_connection_3",
        "http_connection_4",
        "http_connection_5",
    ]


@router.get(
    "/connections/{bh_env_id}/aws_connections", status_code=http_status.HTTP_200_OK
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)

    # TODO will change this later
    return [
        "aws_connection_1",
        "aws_connection_2",
        "aws_connection_3",
        "aws_connection_4",
        "aws_connection_5",
    ]


@router.get(
    "/connections/{bh_env_id}/sftp_connections", status_code=http_status.HTTP_200_OK
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)
    # TODO will change this later
    return [
        "sftp_connection_1",
        "sftp_connection_2",
        "sftp_connection_3",
        "sftp_connection_4",
        "sftp_connection_5",
    ]


@router.get(
    "/connections/{bh_env_id}/snowflake_connections",
    status_code=http_status.HTTP_200_OK,
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)
    # TODO will change this later
    return [
        "snowflake_connection_1",
        "snowflake_connection_2",
        "snowflake_connection_3",
        "snowflake_connection_4",
        "snowflake_connection_5",
    ]


@router.get(
    "/connections/{bh_env_id}/email_connections", status_code=http_status.HTTP_200_OK
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)

    # TODO will change this later
    return [
        "email_connection_1",
        "email_connection_2",
        "email_connection_3",
        "email_connection_4",
        "email_connection_5",
    ]


@router.get(
    "/connections/{bh_env_id}/slack_connections", status_code=http_status.HTTP_200_OK
)
async def test_connection_by_bighammer_project_name(
    *, bh_env_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):

    await ctx.project_environment_service.get_env(id=bh_env_id)

    # TODO will change this later
    return [
        "slack_connection_1",
        "slack_connection_2",
        "slack_connection_3",
        "slack_connection_4",
        "slack_connection_5",
    ]

@router.post(
    "/list-mwaa-environments",
    status_code=http_status.HTTP_200_OK,
)
async def list_mwaa_environments(
    *,
    credentials: AWSCredentials,
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    Endpoint to decrypt credentials and list AWS MWAA environments.
    Args:
        access_key: Encrypted AWS access key.
        secret_access_key: Encrypted AWS secret access key.
        init_vector: Initialization vector for decryption.
        ctx: Application context.
    Returns:
        A list of MWAA environments available in AWS.
    """
    try:
        # Decrypt credentials
        credentials.aws_access_key_id = decrypt_string(credentials.aws_access_key_id, credentials.init_vector)
        credentials.aws_secret_access_key = decrypt_string(credentials.aws_secret_access_key, credentials.init_vector)
    except Exception as e:
        raise DecryptExceptionError(context={"error": str(e)})

    try:
        # Check if AWS credentials are provided
        if credentials.aws_access_key_id and credentials.aws_secret_access_key:
            # Initialize AWSMWAAService with decrypted credentials
            aws_mwaa_service = AWSMWAAService(
                aws_access_key_id=credentials.aws_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key,
                region_name=credentials.location
            )

            # Fetch the list of environments
            environments = aws_mwaa_service.list_environments()
            return {"environments": environments}
        else:
            pass
    except Exception as e:
        raise AWSSecretsClientError(
            context={"message": f"Failed to list MWAA environments: {str(e)}"}
        )


@router.post(
    "/get_aws_mwaa_env_connection",
    status_code=http_status.HTTP_200_OK,
)
async def get_aws_mwaa_env_connection(
    env_name: str,
    credentials: AWSCredentials,
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    Test AWS connections and fetch MWAA environment details.
    Args:
        env_name: The name of the MWAA environment.
        credentials: Encrypted AWS credentials with init_vector.
        authorized: Authorization dependency.
    Returns:
        A success status and MWAA environment details if credentials are valid.
    """
    try:
        # Decrypt AWS credentials
        credentials.aws_access_key_id = decrypt_string(credentials.aws_access_key_id, credentials.init_vector)
        credentials.aws_secret_access_key = decrypt_string(credentials.aws_secret_access_key, credentials.init_vector)
    except Exception as e:
        raise DecryptExceptionError(context={"error": str(e)})

    try:
        # Initialize AWS MWAA service
        aws_mwaa_service = AWSMWAAService(
            aws_access_key_id=credentials.aws_access_key_id,
            aws_secret_access_key=credentials.aws_secret_access_key,
            region_name=credentials.location
        )

        # Test AWS credentials by fetching the MWAA environment details
        environment_details = aws_mwaa_service.get_environment_by_name(env_name)

        if not environment_details:
            raise MwaaEnvironmentNotFoundError(
                context={"env_name": f"Environment '{env_name}' not found."}
            )

        # Return success and environment details
        return {
            "status":"success",
            "environment_details":environment_details
        }

    except Exception as e:
        logger.error(f"Error testing AWS connection or fetching environment details: {e}")
        raise AWSSecretsClientError(
            context={"message": f"Failed to get MWAA environment details: {str(e)}"}
        )
    
