from datetime import datetime
import json
from typing import List, Optional
from urllib.parse import parse_qs
import copy
from app.core.config import Config
from app.exceptions.aws import AWSSecretsClientError
from app.services.aws import AWSS3Service
from app.utils.cloud_service_utils import get_secret_manager_formatted_name
from app.utils.pipeline_utils import pipeline_sample_json
from app.utils.validata_flow_schema import validate_json
from fastapi import APIRouter, Depends, Query, Query, Request
from fastapi import status as http_status
from src.flow import FlowRunner
from app.api.deps import get_context
from app.core.context import Context
from app.enums.flow import SchemaTypes
from app.exceptions.flow import (
    FlowAlreadyExists,
    FlowDoesNotExist,
    JsonNotValidError,
    SchemaDoesNotExist,
)
from app.models.base import StatusMessage
from app.models.flow import (
    FlowBase,
    FlowConfigBase,
    FlowConfigCreate,
    FlowConfigReturn,
    FlowConfigUpdate,
    FlowCreate,
    FlowDefinition,
    FlowDefinitionCreate,
    FlowDefinitionReturn,
    FlowDefinitionUpdate,
    FlowDeploymentBase,
    FlowDeploymentCreate,
    FlowDeploymentReturn,
    FlowDeploymentUpdate,
    FlowReturn,
    FlowUpdate,
    FlowVersionBase,
    FlowVersionCreate,
    FlowVersionReturn,
    FlowVersionUpdate,
)
from app.utils.auth_wrapper import authorize
from app.utils.bh_project import generate_github_secret_name
from app.utils.flow_utils import (
    create_flow_release_version,
    validate_flow_name,
)
from app.utils.moniter_utils import request_create_monitor, store_monitor_data
from app.utils.normalization import normalise_name
from app.utils.constants import AWS, GCP, AZURE, AWS_ID, GCP_ID, AZURE_ID

router = APIRouter()


@router.get(
    "/list/", response_model=List[FlowReturn], status_code=http_status.HTTP_200_OK
)
async def get_all_flows(
    *,
    flow_id: Optional[int] = None,
    flow_name: Optional[str] = None,
    bh_project_id: Optional[int] = None,
    updated_at: Optional[datetime] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'flow_name', 'flow_description'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):

    flows = await ctx.flow_service.list(
        flow_id=flow_id,
        flow_name=flow_name,
        bh_project_id=bh_project_id,
        updated_at=updated_at,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

    # Add the schedule intervals to the flows list
    return flows


@router.get(
    "/{flow_id}", response_model=FlowReturn, status_code=http_status.HTTP_200_OK
)
async def get_flow(
    *,
    flow_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):

    flow = await ctx.flow_service.get(flow_id)
    return flow


@router.get(
    "/flow/search",
    response_model=List[FlowReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_flow_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, flow_name=abc&flow_key=cdf"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.flow_service.search(params=params)


@router.post(
    "/create/", response_model=FlowReturn, status_code=http_status.HTTP_201_CREATED
)
async def create_flow(
    obj: FlowCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
) -> FlowReturn:
    # flow name should be unique
    flow_exist = await ctx.flow_service.check_flow_exists(obj.flow_name)
    if flow_exist:
        raise FlowAlreadyExists(context={"name": obj.flow_name})

    # validate_flow_name(
    #     obj.flow_name
    # )  # validate_flow_name should ne minimum 3 characters and alphanumeric only
    flow_key = normalise_name(obj.flow_name)  # normalize the flow key
    # Create the flow
    new_flow_obj = FlowBase(**obj.dict(), flow_key=flow_key)
    new_flow = await ctx.flow_service.create(new_flow_obj, authorized=authorized)

    bh_project_name = None
    if new_flow.bh_project_id:
        bh_project = await ctx.bh_project_service.get_by_id(new_flow.bh_project_id)
        if bh_project:
            bh_project_name = bh_project.bh_project_name

    # Create monitors for each alert setting
    if new_flow.alert_settings:
        monitor_data_list = store_monitor_data(
            new_flow.flow_id,
            new_flow.bh_project_id,
            bh_project_name,
            new_flow.alert_settings,
            authorized.get("username"),
            new_flow.flow_key,
        )
        for monitor_data in monitor_data_list:
            await request_create_monitor(monitor_data)
    # Create flow definition ,deployment and config
    schema_version = await ctx.schema_service.get_latest_by_type(
        schema_type=SchemaTypes.FLOW.value
    )
    flow_definition_obj = FlowDefinition(
        schema_id=schema_version, flow_json=obj.flow_json, flow_id=new_flow.flow_id
    )
    flow_deployment_obj = FlowDeploymentBase(
        flow_id=new_flow.flow_id, bh_env_id=obj.bh_env_id, schema_id=schema_version
    )
    flow_config_obj = FlowConfigBase(flow_id=new_flow.flow_id, flow_config={})
    await ctx.flow_defination_service.create(
        obj=flow_definition_obj, authorized=authorized
    )
    await ctx.flow_deployment_service.create(
        obj=flow_deployment_obj, authorized=authorized
    )
    await ctx.flow_config_service.create(obj=flow_config_obj, authorized=authorized)

    await ctx.db_session.refresh(new_flow)

    return new_flow

    # TODO : add flow deployment (need to confirm)
    # deployment = None
    # if new_flow:
    #     bh_env_id = obj.bh_env_id
    #     deployment_obj = FlowDeploymentCreate(
    #         **new_flow.dict(), bh_env_id=bh_env_id, flow_lock_status=False
    #     )
    #     deployment = await ctx.flow_deployment_service.create(deployment_obj)

    # # Create schedule interval if provided
    # new_schedule_interval = None
    # if schedule_interval_data:
    #     await ctx.db_session.refresh(new_flow)  # Explicitly fetch if lazy-loaded properties are used
    #     schedule_interval = ScheduleIntervalCreate(**schedule_interval_data.dict())
    #     schedule_interval.flow_id=new_flow.flow_id
    #     new_schedule_interval = await ctx.schedule_interval_service.create(schedule_interval)

    # await ctx.db_session.refresh(new_flow)
    # await ctx.db_session.refresh(deployment)

    # return FlowReturn(
    #     **new_flow.dict(),
    #     schedule_intervals=new_schedule_interval,
    #     flow_deployment=[deployment]
    # )


@router.patch(
    "/{flow_id}", response_model=FlowReturn, status_code=http_status.HTTP_200_OK
)
async def update_flow(
    *,
    flow_id: int,
    obj: FlowUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
) -> FlowReturn:
    # Check if the flow name already exists
    flow_exist = await ctx.flow_service.check_flow_exists(obj.flow_name)
    if flow_exist:
        raise FlowAlreadyExists(context={"name": obj.flow_name})

    # validate_flow_name should ne minimum 3 characters and alphanumeric only
    if obj.flow_name:
        validate_flow_name(obj.flow_name)

    # TODO # validate_json against flow schema
    # validate_json(obj.metadata_flow)
    return await ctx.flow_service.update(id=flow_id, obj=obj, authorized=authorized)


@router.delete(
    "/{flow_id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_flow_by_id(
    flow_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    status = await ctx.flow_service.delete(id=flow_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/flow-deployment/list",
    response_model=List[FlowDeploymentReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_deployments(
    *,
    flow_deployment_id: Optional[int] = None,
    flow_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'flow_name', 'flow_description'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):

    flows = await ctx.flow_deployment_service.list(
        flow_deployment_id=flow_deployment_id,
        flow_id=flow_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

    return flows


@router.get(
    "/flow-deployment/search",
    response_model=List[FlowDeploymentReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_flow_deployment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, flow_id=123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.flow_deployment_service.search(params=params)


@router.get(
    "/flow-deployment/{flow_deployment_id}",
    response_model=FlowDeploymentReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_deployment(
    *,
    flow_deployment_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):

    flow_deployment = await ctx.flow_deployment_service.get(flow_deployment_id)

    return flow_deployment


@router.post(
    "/flow-deployment/create",
    response_model=FlowDeploymentReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_flow_deployment(
    *,
    obj: FlowDeploymentCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    try:
        schema_version = await ctx.schema_service.get_latest_by_type(
            schema_type=SchemaTypes.FLOW.value
        )
    except:
        raise SchemaDoesNotExist()
    flow_deployment_obj = FlowDeploymentBase(schema_id=schema_version, **obj.dict())

    flow_deployment = await ctx.flow_deployment_service.create(
        flow_deployment_obj, authorized=authorized
    )
    return flow_deployment
    # TODO will remove
    # # Create schedule interval if provided
    # if obj.schedule_interval:
    #     schedule_interval = ScheduleIntervalCreate(**obj.schedule_interval.dict())
    #     schedule_interval.flow_deployment_id=flow_deployment.flow_deployment_id
    #     await ctx.schedule_interval_service.create(schedule_interval)
    # await ctx.db_session.refresh(flow_deployment)


@router.patch(
    "/flow-deployment/{flow_deployment_id}",
    response_model=FlowDeploymentReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_deployment(
    *,
    flow_deployment_id: int,
    obj: FlowDeploymentUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    # schedule_interval_update = obj.schedule_interval
    # obj.schedule_interval = None
    # Update the flow deployment
    flow_deployment = await ctx.flow_deployment_service.update(
        flow_deployment_id, obj, authorized=authorized
    )

    return flow_deployment

    # TODO will remove now commiting the code when create flow version
    # Update or create schedule interval if provided
    # if schedule_interval_update:
    #     existing_schedule = await ctx.schedule_interval_service.get_by_flow_deployment_id(flow_deployment_id)
    #     if existing_schedule:
    #         # Update existing schedule interval
    #         schedule_interval_update = ScheduleIntervalUpdate(**schedule_interval_update.dict())
    #         await ctx.schedule_interval_service.update(existing_schedule.id, schedule_interval_update)
    #     else:
    #         # Create a new schedule interval
    #         schedule_interval_create = ScheduleIntervalCreate(schedule_interval_update.dict())
    #         schedule_interval_create.flow_deployment_id = flow_deployment_id
    #         await ctx.schedule_interval_service.create(schedule_interval_create)

    # await ctx.db_session.refresh(flow_deployment)

    # if obj.commit_message and obj.flow_json:
    #     # TODO # validate_json against flow schema
    #     # validate_json(obj.metadata_flow)

    #     dag_json = json_parser(obj.flow_json)  # convert json to dag

    #     flow_deployment = await ctx.flow_deployment_service.get(flow_deployment_id)

    #     flow = await ctx.flow_service.get(flow_deployment.flow_id)

    #     if not flow:
    #         raise FlowDoesNotExist()

    #     environment = await ctx.project_environment_service.get(id=obj.bh_env)

    #     secret_name = get_secret_manager_formatted_name(environment.bh_env_name)
    #     secret_key = await ctx.aws_service.secrets.get_secret(secret_name)
    #     aws_s3_service = AWSS3Service(
    #         secret_key.get("aws_access_key_id", ""),
    #         secret_key.get("aws_secret_access_key", ""),
    #     )

    #     bucket_name = flow.flow_key
    #     file_name = "dag.json"

    #     aws_s3_service.create_bucket_and_upload_json(
    #         bucket_name, file_name, obj.flow_json
    #     )

    #     project = await ctx.bh_project_service.get(flow.bh_project_id)

    #     if not project:
    #         raise BHProjectDoesNotExist()
    #     flow_version = create_flow_release_version(flow_deployment.flow_version)
    #     await ctx.flow_deployment_service.create_commit(
    #         flow, project, flow.git_branch, obj.commit_message, dag_json, flow_version
    #     )
    #     obj.flow_version = flow_version
    #     obj.commit_message = None


@router.delete(
    "/flow-deployment/{flow_deployment_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_deployment_by_id(
    flow_deployment_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    status = await ctx.flow_deployment_service.delete(
        flow_deployment_id, authorized=authorized
    )

    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/flow-definition/list/",
    response_model=List[FlowDefinitionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_flow_definitions(
    *,
    flow_definition_id: Optional[int] = None,
    flow_id: Optional[int] = None,
    schema_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'flow_definition_id', 'flow_id'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_defination_service.list(
        flow_definition_id=flow_definition_id,
        flow_id=flow_id,
        schema_id=schema_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/flow-definition/{flow_definition_id}",
    response_model=FlowDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_definition_by_id(
    *,
    flow_definition_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_defination_service.get(id=flow_definition_id)


@router.post(
    "/flow-definition",
    response_model=FlowDefinitionReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_flow_definition(
    *,
    obj: FlowDefinitionCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    schema_version = await ctx.schema_service.get_latest_by_type(
        schema_type=SchemaTypes.FLOW.value
    )
    flow_definition_obj = FlowDefinition(schema_id=schema_version, **obj.dict())
    #     # TODO # validate_json against flow schema
    #     # validate_json(obj.metadata_flow)

    #     dag_json = json_parser(obj.flow_json)  # convert json to dag deploy to airflow bucket
    return await ctx.flow_defination_service.create(
        obj=flow_definition_obj, authorized=authorized
    )


@router.patch(
    "/flow-definition/{flow_definition_id}",
    response_model=FlowDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_definition(
    *,
    flow_definition_id: int,
    obj: FlowDefinitionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    if not obj.flow_json:
        return await ctx.flow_defination_service.update(
            id=flow_definition_id, obj=obj, authorized=authorized
        )

    # Deep copy flow_json for later restoration
    full_flow_json = copy.deepcopy(obj.flow_json)
    obj.flow_json = obj.flow_json.get("flowJson")

    # Retrieve flow deployment details
    try:
        flow_deployment = (
            await ctx.flow_deployment_service.get_flow_deployment_with_flow(
                obj.flow_deployment_id
            )
        )
    except Exception as e:
        raise ValueError("Failed to fetch flow deployment") from e

    # Determine cloud provider
    cloud_provider_map = {
        AWS_ID: AWS,
        GCP_ID: GCP,
        AZURE_ID: AZURE,
    }  # cloud service add here
    client_cloud_provider = cloud_provider_map.get(
        flow_deployment.project_environment.cloud_provider_cd
    )
    if not client_cloud_provider:
        raise ValueError("Unsupported cloud provider")

    # Generate DAG file from flow JSON
    try:
        cfg = Config()
        flow_runner = FlowRunner(
            config=obj.flow_json,
            bh_app_bucket=cfg.BH_APP_BUCKET,
            client_airflow_bucket=flow_deployment.project_environment.airflow_bucket_name,
            bh_cloud_provider=cfg.CLOUD_TYPE,
            client_cloud_provider=client_cloud_provider,
            pipeline_engine_version=cfg.PIPELINE_ENGINE_VERSION,
            schema_file_path=cfg.SCHEMA_FILE_PATH,
        )
        dag_file = flow_runner.get_dag_code()
    except Exception as e:
        raise JsonNotValidError(context={"error": str(e)})

    # Deploy DAG file based on cloud provider
    try:
        if client_cloud_provider == AWS:
            secret_name = flow_deployment.project_environment.pvt_key
            secret_key = await ctx.aws_service.secrets.get_secret(secret_name)
            aws_s3_service = AWSS3Service(
                secret_key.get("aws_access_key", ""),
                secret_key.get("aws_secret_access_key", ""),
                "us-east-1",
            )
            bucket_name = flow_deployment.project_environment.airflow_bucket_name
            airflow_dag_folder = "dags/"
            dag_file_name = f"{flow_deployment.flow.flow_key}.py"
            # Upload the DAG file to the bucket in the Airflow DAGs folder
            aws_s3_service.upload_file_to_s3(
                bucket_name=bucket_name,
                key=f"{airflow_dag_folder}{dag_file_name}",
                file_content=dag_file,
                content_type="application/x-python-code",
            )
        elif client_cloud_provider == GCP:
            # deploy to gcp
            pass

        elif client_cloud_provider == AZURE:
            # deploy to azure
            pass
    except Exception as e:
        raise AWSSecretsClientError(context={"message": str(e)})

    # Restore full flow JSON before updating
    obj.flow_deployment_id = None
    obj.flow_json = full_flow_json

    return await ctx.flow_defination_service.update(
        id=flow_definition_id, obj=obj, authorized=authorized
    )


@router.delete(
    "/flow-definition/{flow_definition_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_definition_by_id(
    flow_definition_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.flow_defination_service.delete(
        id=flow_definition_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/flow-definition/get-by-flow-id/{flow_id}",
    response_model=FlowDefinitionReturn,  # Replace with a custom schema if needed
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_definition(
    flow_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    """
    Retrieve the FlowDefinition associated with a Flow by its ID.
    """
    flow_definition = await ctx.flow_defination_service.get_flow_definition_by_flow_id(
        flow_id
    )
    return flow_definition


@router.delete(
    "/flow-definition/delete-by-flow-id/{flow_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_definition_by_flow_id(
    flow_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    """
    Delete FlowDefinition by flow_id.
    """
    status = await ctx.flow_defination_service.delete_by_flow_id(
        flow_id=flow_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.patch(
    "/flow-definition/update-by-flow-id/{flow_id}",
    response_model=FlowDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_definition_by_flow_id(
    *,
    flow_id: int,
    obj: FlowDefinitionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    """
    Update FlowDefinition by flow_id.
    """

    if not obj.flow_json:
        return await ctx.flow_defination_service.update_by_flow_id(
            flow_id=flow_id, obj=obj, authorized=authorized
        )

    # Deep copy flow_json for later restoration
    full_flow_json = copy.deepcopy(obj.flow_json)
    obj.flow_json = obj.flow_json.get("flowJson")

    # Retrieve flow deployment details
    try:
        flow_deployment = (
            await ctx.flow_deployment_service.get_flow_deployment_with_flow(
                obj.flow_deployment_id
            )
        )
    except Exception as e:
        raise ValueError("Failed to fetch flow deployment") from e

    # Determine cloud provider
    cloud_provider_map = {
        AWS_ID: AWS,
        GCP_ID: GCP,
        AZURE_ID: AZURE,
    }  # cloud service add here
    client_cloud_provider = cloud_provider_map.get(
        flow_deployment.project_environment.cloud_provider_cd
    )
    if not client_cloud_provider:
        raise ValueError("Unsupported cloud provider")

    # Generate DAG file from flow JSON
    try:
        cfg = Config()
        flow_runner = FlowRunner(
            config=obj.flow_json,
            bh_app_bucket=cfg.BH_APP_BUCKET,
            client_airflow_bucket=flow_deployment.project_environment.airflow_bucket_name,
            bh_cloud_provider=cfg.CLOUD_TYPE,
            client_cloud_provider=client_cloud_provider,
            pipeline_engine_version=cfg.PIPELINE_ENGINE_VERSION,
            schema_file_path=cfg.SCHEMA_FILE_PATH,
        )
        dag_file = flow_runner.get_dag_code()
    except Exception as e:
        raise JsonNotValidError(context={"error": str(e)})

    # Deploy DAG file based on cloud provider
    try:
        if client_cloud_provider == AWS:
            secret_name = flow_deployment.project_environment.pvt_key
            secret_key = await ctx.aws_service.secrets.get_secret(secret_name)
            aws_s3_service = AWSS3Service(
                secret_key.get("aws_access_key", ""),
                secret_key.get("aws_secret_access_key", ""),
                "us-east-1",
            )
            bucket_name = flow_deployment.project_environment.airflow_bucket_name
            airflow_dag_folder = "dags/"
            dag_file_name = f"{flow_deployment.flow.flow_key}.py"
            # Upload the DAG file to the bucket in the Airflow DAGs folder
            aws_s3_service.upload_file_to_s3(
                bucket_name=bucket_name,
                key=f"{airflow_dag_folder}{dag_file_name}",
                file_content=dag_file,
                content_type="application/x-python-code",
            )
        elif client_cloud_provider == GCP:
            # deploy to gcp
            pass

        elif client_cloud_provider == AZURE:
            # deploy to azure
            pass
    except Exception as e:
        raise AWSSecretsClientError(context={"message": str(e)})

    # Restore full flow JSON before updating
    obj.flow_deployment_id = None
    obj.flow_json = full_flow_json

    return await ctx.flow_defination_service.update_by_flow_id(
        flow_id=flow_id, obj=obj, authorized=authorized
    )


@router.get(
    "/flow-version/list/",
    response_model=List[FlowVersionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_flow_versions(
    *,
    flow_version_id: Optional[int] = None,
    flow_id: Optional[int] = None,
    version_tag: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'flow_version_id', 'version_tag'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_version_service.list(
        flow_version_id=flow_version_id,
        flow_id=flow_id,
        version_tag=version_tag,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/flow-version/search",
    response_model=List[FlowVersionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_flow_deployment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, commit_id=##123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.flow_version_service.search(params=params)


@router.get(
    "/flow-version/{flow_version_id}",
    response_model=FlowVersionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_version_by_id(
    *,
    flow_version_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_version_service.get(id=flow_version_id)


@router.post(
    "/flow-version",
    response_model=FlowVersionReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_flow_version(
    *,
    obj: FlowVersionCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):

    flow_deployment = await ctx.flow_deployment_service.get_flow_deployment_with_flow(
        obj.flow_deployment_id
    )

    if not flow_deployment:
        raise FlowDoesNotExist()
    flow_json = flow_deployment.flow.flow_definition.flow_json.get("flowJson")
    # Determine cloud provider
    cloud_provider_map = {
        AWS_ID: AWS,
        GCP_ID: GCP,
        AZURE_ID: AZURE,
    }  # cloud service add here
    client_cloud_provider = cloud_provider_map.get(
        flow_deployment.project_environment.cloud_provider_cd
    )
    if not client_cloud_provider:
        raise ValueError("Unsupported cloud provider")

    flow_json = copy.deepcopy(flow_json)
    try:
        cfg = Config()
        flow_runner = FlowRunner(
            config=flow_json,
            bh_app_bucket=cfg.BH_APP_BUCKET,
            client_airflow_bucket=flow_deployment.project_environment.airflow_bucket_name,
            bh_cloud_provider=cfg.CLOUD_TYPE,
            client_cloud_provider=client_cloud_provider,
            pipeline_engine_version=cfg.PIPELINE_ENGINE_VERSION,
            schema_file_path=cfg.SCHEMA_FILE_PATH,
        )
        dag_file = flow_runner.get_dag_code()
    except Exception as e:
        raise JsonNotValidError(context={"error": str(e)})
    version_tag = create_flow_release_version()
    secret_name = generate_github_secret_name(
        flow_deployment.flow.bh_project.bh_project_name
    )  # get secret name

    secret_data = await ctx.aws_service.secrets.get_secret(secret_name)

    github_token = secret_data.get("github_token")

    response = await ctx.flow_deployment_service.create_commit(
        flow_deployment.flow,
        flow_deployment.flow.bh_project,
        flow_deployment.flow.bh_project.bh_default_branch,
        obj.comment,
        flow_json,
        github_token,
        dag_file,
    )

    flow_version_obj = FlowVersionBase(
        version_tag=version_tag,
        comment=obj.comment,
        flow_json=flow_deployment.flow.flow_definition.flow_json,
        commit_id=response.get("commit_id", ""),
    )

    flow_version = await ctx.flow_version_service.create(
        obj=flow_version_obj, authorized=authorized
    )
    # Update the FlowDeployment's flow_version_id with the new FlowVersion's ID
    flow_deployment = await ctx.flow_deployment_service.get(obj.flow_deployment_id)
    flow_deployment_update = FlowDeploymentUpdate(
        flow_version_id=flow_version.flow_version_id
    )
    await ctx.flow_deployment_service.update(
        flow_deployment.flow_deployment_id,
        flow_deployment_update,
        authorized=authorized,
    )
    await ctx.db_session.refresh(flow_version)
    return flow_version


@router.put(
    "/flow-version/{flow_version_id}",
    response_model=FlowVersionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_version_by_id(
    *,
    flow_version_id: int,
    obj: FlowVersionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    return await ctx.flow_version_service.update(
        id=flow_version_id, obj=obj, authorized=authorized
    )


@router.delete(
    "/flow-version/{flow_version_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_version_by_id(
    flow_version_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.flow_version_service.delete(
        id=flow_version_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/flow-config/list/",
    response_model=List[FlowConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_flow_configs(
    *,
    flow_config_id: Optional[int] = None,
    flow_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'flow_config_id', 'flow_id'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_config_service.list(
        flow_config_id=flow_config_id,
        flow_id=flow_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/flow-config/search",
    response_model=List[FlowConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_flow_deployment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, flow_id=##123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.flow_config_service.search(params=params)


@router.get(
    "/flow-config/{flow_config_id}",
    response_model=FlowConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_flow_config(
    *,
    flow_config_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    return await ctx.flow_config_service.get(id=flow_config_id)


@router.post(
    "/flow-config/",
    response_model=FlowConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_flow_config(
    *,
    obj: FlowConfigCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    return await ctx.flow_config_service.create(obj=obj, authorized=authorized)


@router.put(
    "/flow-config/{flow_config_id}",
    response_model=FlowConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_flow_config(
    *,
    flow_config_id: int,
    obj: FlowConfigUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    return await ctx.flow_config_service.update(
        id=flow_config_id, obj=obj, authorized=authorized
    )


@router.delete(
    "/flow-config/{flow_config_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_flow_config(
    *,
    flow_config_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.flow_config_service.delete(
        id=flow_config_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}
