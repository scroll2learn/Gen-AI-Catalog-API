import json
from datetime import datetime
from typing import List, Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi import status as http_status
from fastapi.responses import StreamingResponse

from app.api.deps import get_context
from app.core.context import Context
from app.enums.flow import SchemaTypes
from app.enums.pipeline import ParameterType
from app.exceptions.bh_project import BHProjectDoesNotExist
from app.exceptions.pipeline import PipelineAlreadyExists, PipelineDoesNotExist, SchemaDoesNotExist
from app.models.base import StatusMessage
from app.models.pipelines import (PipelineBase, PipelineConfigBase, PipelineConnectionCreate, PipelineConnectionReturn, PipelineConnectionUpdate, PipelineCreate, PipelineUpdate, PipelineReturn, 
                                  PipelineDefinition,
                                  PipelineDefinitionCreate,
                                  PipelineDefinitionUpdate,
                                  PipelineDefinitionReturn, 
                                  PipelineConfig, PipelineConfigCreate, PipelineConfigReturn, PipelineConfigUpdate,
                                  PipelineVersion, PipelineVersionBase, PipelineVersionCreate, PipelineVersionUpdate, PipelineVersionReturn, PipelineValidationErrorReturn,
                                  PipelineParameterBase, PipelineParameterCreate, PipelineParameterReturn, PipelineParameterUpdate,
                                  )
from app.services.aws import AWSS3Service
from app.services.pipelines import PipelineDebugService, PipelineLogService
from app.utils.bh_project import generate_github_secret_name
from app.utils.pipeline_utils import(create_pipeline_release_version, validate_pipeline_name)
from app.utils.auth_wrapper import authorize
from app.utils.git_utils.git_utils import extract_secret_name
from app.utils.normalization import normalise_name
from app.utils.data_source_utils import get_text_embedding

router = APIRouter()


@router.get(
    "/list/",
    response_model=List[PipelineReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_pipelines(
    *,
    pipeline_id: Optional[int] = None,
    pipeline_name: Optional[str] = None,
    bh_project_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None,
        description="Field to order by, e.g., 'pipeline_name', 'pipeline_description'",
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.pipeline_service.list(
        pipeline_id=pipeline_id,
        pipeline_name=pipeline_name,
        bh_project_id=bh_project_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )


@router.get(
    "/search/",
    response_model=List[PipelineReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
    *,
    params: Optional[str] = Query(
        None,
        description="Search any field like, 'pipeline_name', 'pipeline_description'",
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.pipeline_service.search(params=params)


@router.get(
    "/{pipeline_id}",
    response_model=PipelineReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_by_id(
    *, pipeline_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    pipeline = await ctx.pipeline_service.get(pipeline_id)
    return pipeline


@router.post(
    "/",
    response_model=PipelineReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_pipeline(
    *, pipeline_in: PipelineCreate, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
) -> PipelineReturn:
    # Get the project using the project ID
    project = await ctx.bh_project_service.get(pipeline_in.bh_project_id)
    if not project:
        raise BHProjectDoesNotExist(status_code=404, detail="Project not found")

    pipeline_exist = await ctx.pipeline_service.check_pipeline_exists(
        pipeline_in.pipeline_name
    )
    if pipeline_exist:
        raise PipelineAlreadyExists(context={"name": pipeline_in.pipeline_name})
    

    pipeline_key = normalise_name(pipeline_in.pipeline_name)
    embedding = await get_text_embedding(pipeline_in.pipeline_name)
    new_pipeline_in = PipelineBase(
        **pipeline_in.dict(),
        pipeline_key=pipeline_key,
        pipeline_name_embedding=embedding
        )
    new_pipeline = await ctx.pipeline_service.create(new_pipeline_in, authorized=authorized)

    try:
        schema_version = await ctx.schema_service.get_latest_by_type(
            schema_type=SchemaTypes.PIPELINE.value
        )
    except:
        raise SchemaDoesNotExist()
    
    pipeline_definition_obj = PipelineDefinition(
        schema_id=schema_version, pipeline_json=pipeline_in.pipeline_json, pipeline_id=new_pipeline.pipeline_id
    )
    

    pipeline_config_obj = PipelineConfigBase(pipeline_id=new_pipeline.pipeline_id, pipeline_config={})

    await ctx.pipeline_definition_service.create(
        obj = pipeline_definition_obj, authorized=authorized
    )

    await ctx.pipeline_config_service.create(
        obj = pipeline_config_obj, authorized=authorized
    )

    await ctx.db_session.refresh(new_pipeline)

    return new_pipeline

@router.patch(
    "/{pipeline_id}", response_model=PipelineReturn, status_code=http_status.HTTP_200_OK
)
async def update_pipeline(
    *,
    pipeline_id: int,
    obj: PipelineUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
) -> PipelineReturn:
    # Check if the flow name already exists
    pipeline_exist = await ctx.pipeline_service.check_pipeline_exists(obj.pipeline_name)
    if pipeline_exist:
        raise PipelineAlreadyExists(context={"name": obj.pipeline_name})
    
    if obj.pipeline_name:
        validate_pipeline_name(obj.pipeline_name)

    # TODO # validate_json against pipeline schema
    # validate_json(obj.metadata_pipline)
    return await ctx.pipeline_service.update(id=pipeline_id, obj=obj, authorized=authorized)
     

# @router.put(
#     "/{pipeline_id}",
#     response_model=PipelinesReturn,
#     status_code=http_status.HTTP_200_OK,
# )
# async def update_pipeline(
#     *,
#     pipeline_id: int,
#     pipeline_in: PipelineUpdate,
#     ctx: Context = Depends(get_context),
#     authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
# ):
#     return await ctx.pipeline_service.update(pipeline_id, pipeline_in, authorized=authorized)


# @router.put(
#     "/auto-save/{pipeline_id}",
#     status_code=http_status.HTTP_200_OK,
# )
# async def update_pipeline_auto_save(
#     *,
#     pipeline_id: int,
#     pipeline_in: PipelineDefinationAutosave,
#     ctx: Context = Depends(get_context),
#     authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
# ):
#     # TODO: From the JWT, get user details, update definition in the current row
#     pipeline_defination = await ctx.pipeline_service.check_pipeline_defination_exists(
#         pipeline_id
#     )
#     if not pipeline_defination:
#         pipeline_defination = await ctx.pipeline_definition_service.create(
#             PipelineDefinationCreate(
#                 pipeline_id=pipeline_id, pipeline_json=pipeline_in.pipeline_json
#             ), authorized=authorized
#         )
#     await ctx.pipeline_service.update_auto_save(
#         pipeline_defination, pipeline_in.pipeline_json
#     )
#     return {"status": http_status.HTTP_200_OK, "detail": "success"}


@router.delete(
    "/{pipeline_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_pipeline(
    *, pipeline_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    status = await ctx.pipeline_service.delete(pipeline_id, authorized=authorized)
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "pipeline_defination/{pipeline_id}",
    response_model=List[PipelineDefinitionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_defination(
    *, pipeline_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    return await ctx.pipeline_service.get_pipeline_defination(pipeline_id)



@router.get(
    "/pipeline-definition/list/",
    response_model=List[PipelineDefinitionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_pipeline_definitions(
    *,
    pipeline_definition_id: Optional[int] = None,
    pipeline_id: Optional[int] = None,
    schema_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'pipeline_definition_id', 'pipeline_id'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_definition_service.list(
        pipeline_definition_id=pipeline_definition_id,
        pipeline_id=pipeline_id,
        schema_id=schema_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

@router.get(
    "/pipeline-definition/{pipeline_definition_id}",
    response_model=PipelineDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_definition_by_id(
    *,
    pipeline_definition_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_definition_service.get(id=pipeline_definition_id)

@router.post(
    "/pipeline-definition",
    response_model=PipelineDefinitionReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_pipeline_definition(
    *,
    obj: PipelineDefinitionCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    schema_version = await ctx.schema_service.get_latest_by_type(schema_type=SchemaTypes.PIPELINE.value)
    pipeline_definition_obj = PipelineDefinition(schema_id=schema_version, **obj.dict())
    return await ctx.pipeline_definition_service.create(
        obj=pipeline_definition_obj, authorized=authorized
    )

@router.patch(
    "/pipeline-definition/{pipeline_definition_id}",
    response_model=PipelineDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_pipeline_definition(
    *,
    pipeline_definition_id: int,
    obj: PipelineDefinitionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
 
    return await ctx.pipeline_definition_service.update(
        id=pipeline_definition_id, obj=obj, authorized=authorized
    )

@router.delete(
    "/pipeline-definition/{pipeline_definition_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_pipeline_definition_by_id(
    pipeline_definition_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.pipeline_definition_service.delete(
        id=pipeline_definition_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/pipeline-definition/get-by-pipeline-id/{pipeline_id}",
    response_model=PipelineDefinitionReturn,  # Replace with a custom schema if needed
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_definition(
    pipeline_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
):
    """
    Retrieve the pipelineDefinition associated with a pipeline by its ID.
    """
    pipeline_definition = await ctx.pipeline_definition_service.get_pipeline_definition_by_pipeline_id(
        pipeline_id
    )
    return pipeline_definition


@router.delete(
    "/pipeline-definition/delete-by-pipeline-id/{pipeline_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_pipeline_definition_by_pipeline_id(
    pipeline_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    """
    Delete pipelineDefinition by pipeline_id.
    """
    status = await ctx.pipeline_definition_service.delete_by_pipeline_id(
        pipeline_id=pipeline_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.put(
    "/pipeline-definition/update-by-pipeline-id/{pipeline_id}",
    response_model=PipelineDefinitionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_pipeline_definition_by_pipeline_id(
    *,
    pipeline_id: int,
    obj: PipelineDefinitionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    """
    Update pipelineDefinition by pipeline_id.
    """
    return await ctx.pipeline_definition_service.update_by_pipeline_id(
        pipeline_id=pipeline_id, obj=obj, authorized=authorized
    )


@router.get(
    "/pipeline-config/list/",
    response_model=List[PipelineConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_pipeline_configs(
    *,
    pipeline_config_id: Optional[int] = None,
    pipeline_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'pipeline_config_id', 'pipeline_id'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_config_service.list(
        pipeline_config_id=pipeline_config_id,
        pipeline_id=pipeline_id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

@router.get(
    "/pipeline-config/search",
    response_model=List[PipelineConfigReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_pipeline_deployment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, pipeline_id=##123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.pipeline_config_service.search(params=params)


@router.get(
    "/pipeline-config/{pipeline_config_id}",
    response_model=PipelineConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_config(
    *,
    pipeline_config_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_config_service.get(id=pipeline_config_id)

@router.post(
    "/pipeline-config/",
    response_model=PipelineConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def create_pipeline_config(
    *,
    obj: PipelineConfigCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.pipeline_config_service.create(obj=obj, authorized=authorized)

@router.put(
    "/pipeline-config/{pipeline_config_id}",
    response_model=PipelineConfigReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_pipeline_config(
    *,
    pipeline_config_id: int,
    obj: PipelineConfigUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.pipeline_config_service.update(
        id=pipeline_config_id, obj=obj, authorized=authorized
    )

@router.delete(
    "/pipeline-config/{pipeline_config_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_pipeline_config(
    *,
    pipeline_config_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    status = await ctx.pipeline_config_service.delete(
        id=pipeline_config_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


@router.get(
    "/pipeline-version/list/",
    response_model=List[PipelineVersionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def get_all_pipeline_versions(
    *,
    pipeline_version_id: Optional[int] = None,
    pipeline_id: Optional[int] = None,
    version_tag: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    order_by: Optional[str] = Query(
        None, description="Field to order by, e.g., 'pipeline_version_id', 'version_tag'"
    ),
    order_desc: bool = False,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_version_service.list(
        pipeline_version_id=pipeline_version_id,
        pipeline_id=pipeline_id,
        version_tag=version_tag,
        offset=offset,
        limit=limit,
        order_by=order_by,
        order_desc=order_desc,
    )

@router.get(
    "/pipeline-version/search",
    response_model=List[PipelineVersionReturn],
    status_code=http_status.HTTP_200_OK,
)
async def search_pipeline_deployment_field_for_word(
    *,
    params: Optional[str] = Query(
        None, description="Search any field like, commit_id=##123"
    ),
    request: Request,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    if params is not None:
        params = parse_qs(params)
    else:
        params = parse_qs(request.url.query)
    return await ctx.pipeline_version_service.search(params=params)

@router.get(
    "/pipeline-version/{pipeline_version_id}",
    response_model=PipelineVersionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_version_by_id(
    *,
    pipeline_version_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "view"))
):
    return await ctx.pipeline_version_service.get(id=pipeline_version_id)

@router.post(
    "/pipeline-version",
    response_model=PipelineVersionReturn,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_pipeline_version(
    *,
    obj: PipelineVersionCreate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    pipeline = await ctx.pipeline_service.get_pipeline(
        obj.pipeline_id
    )
    
    if not pipeline:
        raise PipelineDoesNotExist
    
    version_tag = create_pipeline_release_version()
    secret_name = generate_github_secret_name(
        pipeline.bh_project.bh_project_name
    )

    secret_data = await ctx.aws_service.secrets.get_secret(secret_name)
    print("secret data", secret_data)
    github_token = secret_data.get("github_token")
    print("github token", github_token)

    if not pipeline.pipeline_definitions:
        raise ValueError("No pipeline definition found")
    
    response = await ctx.pipeline_service.create_commit(
        pipeline,
        pipeline.bh_project,
        pipeline.bh_project.bh_default_branch,
        obj.comment,
        pipeline.pipeline_definitions.pipeline_json,
        github_token,
    )
    print("response", response)
    
    pipeline_version_obj = PipelineVersionBase(
        version_tag=version_tag,
        comment=obj.comment,
        pipeline_json=pipeline.pipeline_definitions.pipeline_json,
        commit_id=response.get("commit_id", ""),
    )

    pipeline_version = await ctx.pipeline_version_service.create(
        obj=pipeline_version_obj, authorized=authorized
    )

    pipeline = await ctx.pipeline_service.get(obj.pipeline_id)
    pipeline_update = PipelineUpdate(
        pipeline_version_id=pipeline_version.pipeline_version_id
    )

    await ctx.pipeline_service.update(
        pipeline.pipeline_id,
        pipeline_update,
        authorized=authorized,
    )
    await ctx.db_session.refresh(pipeline_version)
    return pipeline_version


@router.put(
    "/pipeline-version/{pipeline_version_id}",
    response_model=PipelineVersionReturn,
    status_code=http_status.HTTP_200_OK,
)
async def update_pipeline_version_by_id(
    *,
    pipeline_version_id: int,
    obj: PipelineVersionUpdate,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit"))
):
    return await ctx.pipeline_version_service.update(
        id=pipeline_version_id, obj=obj, authorized=authorized
    )

@router.delete(
    "/pipeline-version/{pipeline_version_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_pipeline_version_by_id(
    pipeline_version_id: int,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    status = await ctx.pipeline_version_service.delete(
        id=pipeline_version_id, authorized=authorized
    )
    return {"status": status, "message": "The record has been deleted!"}


# Run and debug the pipeline 
# @router.post(
#     "/create_commit",
#     response_model=StatusMessage,
#     status_code=http_status.HTTP_200_OK,
# )
# async def create_pipeline_commit(
#     *, obj: PipelineCreate, ctx: Context = Depends(get_context),
#     authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
# ):

#     pipeline = await ctx.pipeline_service.get(obj.pipeline_id)
#     project = pipeline.bh_project
#     if not project:
#         raise BHProjectDoesNotExist(status_code=404, detail="Project not found")

#     secret_name = extract_secret_name(
#         project.bh_github_token_url
#     )  # Extract the secret name from the secret path

#     secret_token = await ctx.gcp_service.secrets.get_secret(
#         secret_name
#     )  # Get the secret token from the secret manager

#     project.bh_github_token_url = secret_token

#     response = await ctx.pipeline_service.create_commit(
#         pipeline, project, obj.git_branch
#     )

#     status = "true" if response.get("status") == 201 else "false"
#     return {"status": status, "message": response.get("message", "Unknown error")}


@router.get(
    "/validate/{pipeline_id}/",
    response_model=PipelineValidationErrorReturn,
    status_code=http_status.HTTP_200_OK,
)
async def validate_pipeline(
    *, pipeline_id: int, ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    # TODO: validate json
    return await ctx.pipeline_service.validate_pipeline(pipeline_id)


@router.post(
    "/debug/start_pipeline",
    status_code=http_status.HTTP_200_OK,
)
async def start_pipeline(
    *,
    pipeline_id: Optional[int] = None,
    pipeline_name: Optional[str] = None,
    pipeline_json: Optional[str] = None,
    mode: str, 
    checkpoints: List[str] = Query([]), 
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
    host: str = 'host.docker.internal',
    port: int = 15003):
    try:
        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )
        # Validate the input parameters
        if not pipeline_id and (not pipeline_name or not pipeline_json):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or both pipeline_name and pipeline_json must be provided."
            )

        # Fetch pipeline details if pipeline_id is provided
        if pipeline_id:
            pipeline = await ctx.pipeline_service.get(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
                 
            pipeline_name = pipeline.pipeline_name
            pipeline_json = json.dumps(pipeline.pipeline_json)

        # Fetch pipeline parameters by pipeline name
        parameters_list = await ctx.pipeline_parameter_service.get_pipeline_parameters_by_pipeline_name(pipeline_name)
        
        user_parameters = [] 
        spark_session_config = {}

        # Separate parameters based on their type
        for parameter in parameters_list:
            if parameter.parameter_type == ParameterType.USER:
                user_parameters.append({
                    'key': parameter.parameter_name,
                    'value': parameter.parameter_value
                })
            elif parameter.parameter_type == ParameterType.SPARK_SESSION:
                parameter_value = parameter.parameter_value
                if parameter_value.isdigit():
                    parameter_value = int(parameter_value)
                spark_session_config[parameter.parameter_name] = parameter_value

        # Parse the pipeline_json
        pipeline_data = json.loads(pipeline_json)

        # Add user parameters to the pipeline JSON
        if user_parameters:
            pipeline_data['parameters'] = user_parameters

        # Add spark_session parameters to the pipeline JSON
        if spark_session_config:
            pipeline_data['spark_session_config'] = spark_session_config

        # Convert the updated pipeline data back to JSON
        pipeline_json = json.dumps(pipeline_data)

        # Start the pipeline
        pipeline_debug_service = PipelineDebugService(host, port)
        message = await pipeline_debug_service.start_pipeline(pipeline_name, pipeline_json, mode, checkpoints)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
        "/debug/stop_pipeline",
        status_code=http_status.HTTP_200_OK,
)
async def stop_pipeline(pipeline_id: Optional[int] = None,
                        pipeline_name: Optional[str] = None,
                        host:str = 'host.docker.internal', 
                        port:int = 15003, 
                        ctx: Context = Depends(get_context),
                        authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))

                        ):
    try:

        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )

        if pipeline_id:
            pipeline = await ctx.pipeline_service.get_pipeline(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
            pipeline_name = pipeline.pipeline_name

        if not pipeline_name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or pipeline_name must be provided."
            )
    
        pipeline_debug_service = PipelineDebugService(host, port)
        message = await pipeline_debug_service.stop_pipeline(pipeline_name)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
        "/debug/get_transformation_output",
        status_code=http_status.HTTP_200_OK,
)
async def get_transformation_output(
    pipeline_id: Optional[int] = None,
    pipeline_name: Optional[str] = None,
    transformation_name: str = Query(...),
    page: int = Query(...),
    page_size: int = Query(...),
    sort_columns: List[str] = Query([]),
    host:str = 'host.docker.internal',
    port:int = 15003,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    try:

        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )

        if pipeline_id:
            pipeline = await ctx.pipeline_service.get_pipeline(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
            pipeline_name = pipeline.pipeline_name

        if not pipeline_name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or pipeline_name must be provided."
            )
        
        pipeline_debug_service = PipelineDebugService(host, port)
        response = await pipeline_debug_service.get_transformation_output(pipeline_name, transformation_name, page, page_size, sort_columns)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
        "/debug/get_transformation_count",
        status_code=http_status.HTTP_200_OK,
)
async def get_transformation_count(pipeline_id: Optional[int] = None,
                                   pipeline_name: Optional[str] = None,
                                   host:str = 'host.docker.internal', 
                                   port:int = 15003, 
                                   ctx: Context = Depends(get_context),
                                   authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))):
    try:

        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )

        if pipeline_id:
            pipeline = await ctx.pipeline_service.get_pipeline(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
            pipeline_name = pipeline.pipeline_name

        if not pipeline_name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or pipeline_name must be provided."
            )
        
        pipeline_debug_service = PipelineDebugService(host, port)
        response = await pipeline_debug_service.get_transformation_count(pipeline_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/run-next-checkpoint",
    status_code=http_status.HTTP_200_OK,
)
async def run_next_checkpoint(
    pipeline_id: Optional[int] = None,
    pipeline_name: Optional[str] = None,
    host:str = 'host.docker.internal',
    port:int = 15003,
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    try:

        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )

        if pipeline_id:
            pipeline = await ctx.pipeline_service.get_pipeline(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
            pipeline_name = pipeline.pipeline_name

        if not pipeline_name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or pipeline_name must be provided."
            )
        
        pipeline_debug_service = PipelineDebugService(host, port)
        message = await pipeline_debug_service.run_next_checkpoint(pipeline_name)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/stream-logs/{pipeline_name}",
    status_code=http_status.HTTP_200_OK,
)
async def stream_logs(
    pipeline_id: Optional[int] = None,
    pipeline_name: Optional[str] = None,
    host:str = 'host.docker.internal',
    port:int = 15003,
    authorized: Optional[dict] = Depends(authorize('admin_module', 'view'))
):
    try:

        if not authorized:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access."
            )

        if pipeline_id:
            pipeline = await ctx.pipeline_service.get_pipeline(pipeline_id)
            if not pipeline:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=f"Pipeline with ID {pipeline_id} not found."
                )
            pipeline_name = pipeline.pipeline_name

        if not pipeline_name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Either pipeline_id or pipeline_name must be provided."
            )
        
        pipeline_log_service = PipelineLogService(host, port)
        log_generator = pipeline_log_service.stream_logs(pipeline_name)

        async def event_generator():
            async for log_line in log_generator:
                yield f"data: {log_line}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get(
        "/pipeline-connection/list/",
        response_model=List[PipelineConnectionReturn],
        status_code=http_status.HTTP_200_OK,
)
async def get_all_pipeline_connections(
                *,
                pipeline_connection_id: Optional[int] = None,
                logical_name: Optional[str] = None,
                connection_type: Optional[str] = None,
                bh_env_id: Optional[int] = None,
                client_project_id: Optional[str] = None,
                offset: int = 0,
                limit: int = 10,
                order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'pipeline_connection_id', 'logical_name'"),
                order_desc: bool = False,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_connection_service.list(
              pipeline_connection_id=pipeline_connection_id,
              logical_name=logical_name,
              connection_type=connection_type,
              bh_env_id=bh_env_id,
              client_project_id=client_project_id,
              offset=offset,
              limit=limit,
              order_by=order_by,
              order_desc=order_desc,
        )


@router.get(
        "/pipeline-connection/search",
        response_model=List[PipelineConnectionReturn],
        status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
                *,
                params: Optional[str] = Query(None, description="Search any field like, logical_name=abc&connection_type=cdf"),
                request: Request,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        if params is not None:
              params = parse_qs(params)
        else:
              params = parse_qs(request.url.query)
        return await ctx.pipeline_connection_service.search(params=params)


@router.get(
        "/pipeline-connection/{pipeline_connection_id}",
        response_model=PipelineConnectionReturn,
        status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_connection(
                *,
                pipeline_connection_id: int,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_connection_service.get(id=pipeline_connection_id)


@router.post(
        "/pipeline-connection",
        response_model=PipelineConnectionReturn,
        status_code=http_status.HTTP_200_OK,
)
async def create_pipeline_connection(
                *,
                obj: PipelineConnectionCreate,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_connection_service.create(obj=obj, authorized=authorized)


@router.put(
    "/pipeline-connection/{pipeline_connection_id}",
    response_model=PipelineConnectionReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_pipeline_connection_by_id(
        *,
        pipeline_connection_id: int,
        obj: PipelineConnectionUpdate,
        authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
        ctx: Context = Depends(get_context)):
    return await ctx.pipeline_connection_service.update(id=pipeline_connection_id, obj=obj, authorized=authorized)


@router.delete(
    "/pipeline-connection/{pipeline_connection_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_pipeline_connection_by_id(
        pipeline_connection_id: int,
        authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
        ctx: Context = Depends(get_context)):
    status = await ctx.pipeline_connection_service.delete(id=pipeline_connection_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}

@router.get(
        "/pipeline-parameter/list/",
        response_model=List[PipelineParameterReturn],
        status_code=http_status.HTTP_200_OK,
)
async def get_all_pipeline_parameters(
                *,
                pipeline_parameter_id: Optional[int] = None,
                parameter_name: Optional[str] = None,
                pipeline_id: Optional[int] = None,
                offset: int = 0,
                limit: int = 10,
                order_by: Optional[str] = Query(None, description="Field to order by, e.g., 'pipeline_parameter_id', 'logical_name'"),
                order_desc: bool = False,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.list(
              pipeline_parameter_id=pipeline_parameter_id,
              parameter_name=parameter_name,
              pipeline_id=pipeline_id,
              offset=offset,
              limit=limit,
              order_by=order_by,
              order_desc=order_desc,
        )


@router.get(
        "/pipeline-parameter/search",
        response_model=List[PipelineParameterReturn],
        status_code=http_status.HTTP_200_OK,
)
async def search_field_for_word(
                *,
                params: Optional[str] = Query(None, description="Search any field like, name=abc&pipeline_id=cdf"),
                request: Request,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        if params is not None:
              params = parse_qs(params)
        else:
              params = parse_qs(request.url.query)
        return await ctx.pipeline_parameter_service.search(params=params)


@router.get(
        "/pipeline-parameter/{pipeline_parameter_id}",
        response_model=PipelineParameterReturn,
        status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_parameter_by_id(
                *,
                pipeline_parameter_id: int,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.get(id=pipeline_parameter_id)


@router.post(
        "/pipeline-parameter",
        response_model=PipelineParameterReturn,
        status_code=http_status.HTTP_200_OK,
)
async def create_pipeline_parameter(
                *,
                obj: PipelineParameterCreate,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.create(obj=obj, authorized=authorized)


@router.put(
    "/pipeline-parameter/{pipeline_parameter_id}",
    response_model=PipelineParameterReturn,
    status_code=http_status.HTTP_200_OK
)
async def update_pipeline_parameter_by_id(
        *,
        pipeline_parameter_id: int,
        obj: PipelineParameterUpdate,
        authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
        ctx: Context = Depends(get_context)):
    return await ctx.pipeline_parameter_service.update(id=pipeline_parameter_id, obj=obj, authorized=authorized)


@router.delete(
    "/pipeline-parameter/{pipeline_parameter_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_pipeline_parameter_by_id(
        pipeline_parameter_id: int,
        authorized: Optional[dict] = Depends(authorize('admin_module', 'edit')),
        ctx: Context = Depends(get_context)):
    status = await ctx.pipeline_parameter_service.delete(id=pipeline_parameter_id, authorized=authorized)

    return {"status": status, "message": "The record has been deleted!"}


@router.get(
        "/pipeline-parameters/{pipeline_id}",
        response_model=List[PipelineParameterReturn],
        status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_parameters_by_pipeline_id(
                *,
                pipeline_id: int,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.get_pipeline_parameters(pipeline_id)


@router.get(
        "/pipeline-parameters/{pipeline_id}/parameter_type/{parameter_type}",
        response_model=List[PipelineParameterReturn],
        status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_parameter_by_type(
                *,
                pipeline_id: int,
                parameter_type: ParameterType,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.get_pipeline_parameters_by_type(pipeline_id, parameter_type)


@router.get(
        "/pipeline-parameters/{pipeline_id}/parameter_name/{name}",
        response_model=PipelineParameterReturn,
        status_code=http_status.HTTP_200_OK,
)
async def get_pipeline_parameter_by_name(
                *,
                pipeline_id: int,
                parameter_name: str,
                authorized: Optional[dict] = Depends(authorize('admin_module', 'view')),
                ctx: Context = Depends(get_context)):
        return await ctx.pipeline_parameter_service.get_pipeline_parameter_by_name(pipeline_id, parameter_name)
