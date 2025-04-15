import json
from app.core.config import Config
from app.utils.data_source_utils import get_text_embedding
import grpc
from typing import List, Optional, Dict
from app.enums.pipeline import ParameterType
from app.exceptions.base import ObjectNotFound
from app.models.bh_project import BHProject
from app.models.pipelines import (
    Pipeline,
    PipelineConnection,
    PipelineConnectionCreate,
    PipelineConnectionReturn,
    PipelineConnectionUpdate,
    PipelineCreate,
    PipelineUpdate,
    PipelineReturn,
    PipelineDefinition,
    PipelineDefinitionCreate,
    PipelineDefinitionUpdate,
    PipelineDefinitionReturn,
    PipelineVersion,
    PipelineVersionCreate,
    PipelineVersionUpdate,
    PipelineVersionReturn,
    PipelineConfig,
    PipelineConfigCreate,
    PipelineConfigUpdate,
    PipelineConfigReturn,
    PipelineParameter,
    PipelineParameterCreate,
    PipelineParameterUpdate,
    PipelineParameterReturn,
)
from app.protos import (
    data_pb2,
    data_pb2_grpc,
    log_pb2,
    log_pb2_grpc,
    pipeline_operations_pb2,
    pipeline_operations_pb2_grpc,
)
from sqlalchemy.orm import joinedload
from app.services.base import BaseService
from app.utils.constants import PIPELINE_DIR
from app.utils.git_utils.git_utils import create_git_branch, initialize_git_provider
from google.protobuf.json_format import MessageToDict
from sqlalchemy import or_, select, desc, text
from sqlalchemy.types import BOOLEAN, INTEGER
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance

class PipelinesService(BaseService):
    model: Pipeline = Pipeline
    create_model: PipelineCreate = PipelineCreate
    update_model: PipelineUpdate = PipelineUpdate
    return_schema: PipelineReturn = PipelineReturn
    # name_field: str = 'pipeline_name'

    async def check_pipeline_exists(
        self,
        pipeline_name: str = None,
    ):
        statement = select(self.model).where(self.model.pipeline_name == pipeline_name, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()
        return response
    
    async def list(
        self,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        **kwargs,
    ) -> List[PipelineReturn]:
        query = select(self.model).options(
            joinedload(self.model.bh_project),
            joinedload(self.model.created_by_user),  # Load created_by user details
            joinedload(self.model.updated_by_user),  # Load updated_by user details
        )

        query = query.where(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        for kw, value in kwargs.items():
            if value is not None:
                query = query.where(getattr(self.model, kw) == value)
        
        query = query.offset(offset).limit(limit)

        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)
        pipelines = results.scalars().all()

        return [
            PipelineReturn(
                pipeline_id=pipeline.pipeline_id,
                pipeline_name=pipeline.pipeline_name,
                pipeline_key=pipeline.pipeline_key,
                bh_project_id=pipeline.bh_project_id,
                notes=pipeline.notes,
                tags=pipeline.tags,
                created_at=pipeline.created_at,
                updated_at=pipeline.updated_at,
                created_by=pipeline.created_by,
                updated_by=pipeline.updated_by,
                bh_project_name=pipeline.bh_project.bh_project_name if pipeline.bh_project else None,
                created_by_username=pipeline.created_by_user.username if pipeline.created_by_user else None,
                updated_by_username=pipeline.updated_by_user.username if pipeline.updated_by_user else None,
            ) for pipeline in pipelines
        ]

        
    async def get(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        statement = select(self.model).filter(primary_key_column == id).filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()

        if response is None:
            raise ObjectNotFound(context={
                'column_name': primary_key_column.name,
                'id': id,
                'type': self.model.__name__,
            })

        return response
    
    async def get_definition_by_pipeline_name(self, pipeline_name: str):
        # query to select Pipeline by name
        statement = (
            select(Pipeline)
            .options(joinedload(Pipeline.pipeline_definitions)) 
            .filter(Pipeline.pipeline_name == pipeline_name)
            .filter(Pipeline.is_deleted == False) 
        )

        result = await self.context.db_session.execute(statement)
        pipeline = result.scalar_one_or_none()

        if pipeline is None:
            raise ObjectNotFound(
                context={
                    "column_name": "pipeline_name",
                    "value": pipeline_name,
                    "type": "Pipeline",
                }
            )

        return pipeline


    async def get_pipeline(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        statement = (
            select(self.model)
                .filter(primary_key_column == id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
                .options(
                    joinedload(self.model.pipeline_definitions),
                    joinedload(self.model.bh_project)
            )
        )
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()

        if response is None:
            raise ObjectNotFound(context={
                'column_name': primary_key_column.name,
                'id': id,
                'type': self.model.__name__,
            })

        return response
    
    async def get_by_id(self, id: int, include_deleted: bool = False):
        
        query = select(self.model).where(self.model.pipeline_id == id)
        if not include_deleted:
            query = query.where(or_(self.model.is_deleted == False, self.model.is_deleted == None))  # Exclude soft-deleted
        result = await self.context.db_session.execute(query)
        return result.scalar_one_or_none()
    

    

    async def search(self, params: Dict[str, str]) -> List[PipelineReturn]:
        query = select(self.model).filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))
        vector_search_fields = ['pipeline_name']

        for field, search_key in params.items():
            model_field = getattr(self.model, field)

            if field in vector_search_fields:
                embedding = await get_text_embedding(search_key[0], "")
                if embedding:
                    embedding_str = f'{embedding}'
                    threshold = 0.8 
                 
                    embed_query = f"""
                        SELECT *, pipeline_name_embedding <-> '{embedding_str}'::vector AS distance
                        FROM {Config.DB_SCHEMA}.pipeline
                        WHERE pipeline_name_embedding <-> '{embedding_str}'::vector < '{threshold}'
                        ORDER BY distance ASC
                        LIMIT 10;
                    """
                    results = await self.context.db_session.execute(text(embed_query))
                    rows = results.fetchall()
                    return [PipelineReturn.from_orm(row) for row in rows]
            else:
                # Handle other types of fields (e.g., exact matches, partial matches)
                if model_field.type == INTEGER:
                    query = query.filter(model_field.in_([int(key) for key in search_key]))
                elif model_field.type == BOOLEAN:
                    if str(search_key[0]).lower() == 'true':
                        query = query.filter(model_field.is_(True))
                    elif str(search_key[0]).lower() == 'false':
                        query = query.filter(model_field.is_(False))
                else:
                    query = query.filter(model_field.in_(search_key))

        results = await self.context.db_session.execute(query)
        return [PipelineReturn.from_orm(result) for result in results.scalars()]

    async def get_last_pipeline(self) -> Optional[Pipeline]:
        """Fetch the last pipeline in the database by sequence number."""
        last_pipeline = await self.context.db_session.execute(
            select(Pipeline).where(Pipeline.is_deleted == False).order_by(Pipeline.pipeline_id.desc()).limit(1)
        )
        return last_pipeline.scalar_one_or_none()

    # async def validate_pipeline(self, pipeline_id: int):
    #     pipeline = await self.get(pipeline_id)
    #     if not pipeline:
    #         raise ObjectNotFound
    #     return pipeline


    async def get_pipeline_by_id(self, pipeline_id: int) -> Pipeline:
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        pipeline = result.scalar_one_or_none()
        return pipeline

    
    # async def update_auto_save(
    #         self,
    #         pipeline_defination: PipelineDefinationAutosave,
    #         json: dict
    # ):
    #     pipeline_defination.pipeline_json = json
    #     self.context.db_session.add(pipeline_defination)
    #     await self.context.db_session.commit()
    #     return pipeline_defination

    # async def generate_pipeline_name(
    #         self,
    #         pipeline_name: str = None) -> str:
    #     last_pipeline = await self.get_last_pipeline()
    #     sequence_number = last_pipeline.pipeline_id + 1 if last_pipeline else 1
    #     return f"{pipeline_name}_{sequence_number}"
    
    async def create_commit(
            self,
            pipeline: Pipeline,
            project: BHProject,
            branch: Optional[str] = None,
            commit: str = "Pipeline Commit",
            pipeline_json: Optional[str] = None,
            github_token: Optional[str] = None) -> dict:

        
        git_provider = await initialize_git_provider(project, github_token)
        await create_git_branch(git_provider, branch)

        content_json = json.dumps(pipeline_json)
        file_path = f"pipeline/{pipeline.pipeline_id}/schema/pipeline.json"

        commit_result = await git_provider.update_file(file_path, commit, content_json, branch)
        if commit_result['status'] != 200:
            commit_result = await git_provider.create_initial_commit(file_path, commit, content_json, branch)

        return commit_result
    

class PipelinesDefinitionService(BaseService):
    model: PipelineDefinition = PipelineDefinition
    create_model: PipelineDefinitionCreate = PipelineDefinitionCreate
    update_model: PipelineDefinitionUpdate = PipelineDefinitionUpdate
    return_schema: PipelineDefinitionReturn = PipelineDefinitionReturn

    async def get_pipeline_definition_by_pipeline_id(self, pipeline_id: int) -> PipelineDefinition:
        """
        Retrieve PipelineDefinition by pipeline_id.
        """
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        pipeline_definition = result.scalar_one_or_none()

        if not pipeline_definition:
            raise ObjectNotFound(context={
                'column_name': 'pipeline_id',
                'id': pipeline_id,
                'type': 'PipelineDefinition',
            })

        return pipeline_definition

    async def get_pipeline_defination(
            self,
            pipeline_id: int
    ) -> PipelineDefinition:
        statement = select(PipelineDefinition).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        pipeline = result.scalar_one_or_none()
        return pipeline

    async def check_pipeline_defination_exists(
        self,
        pipeline_id: int,
    ):
        statement = select(PipelineDefinition).where(PipelineDefinition.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        pipeline = result.scalar_one_or_none()
        return pipeline

    async def delete_by_pipeline_id(self, pipeline_id: int, authorized: dict = None):
        """
        Delete PipelineDefinition by pipeline_id.
        """
        
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        pipeline_definition = result.scalar_one_or_none()
        
        if not pipeline_definition:
            raise ObjectNotFound(context={
                'column_name': 'pipeline_id',
                'id': pipeline_id,
                'type': 'PipelineDefinition',
            })
        if authorized:
            pipeline_definition = self.insert_user_fields(pipeline_definition, authorized, type="delete")
        await self.update(id=pipeline_definition.pipeline_definition_id, obj=pipeline_definition, authorized=authorized)

        return True
    

    async def update_by_pipeline_id(self, pipeline_id: int, obj: PipelineDefinitionUpdate, authorized: dict = None):
        """
        Update PipelineDefinition by pipeline_id.
        """
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        existing_obj = result.scalar_one_or_none()
        
        if not existing_obj:
            raise ObjectNotFound(context={
                'column_name': 'pipeline_id',
                'id': pipeline_id,
                'type': 'PipelineDefinition',
            })
        if authorized:
            existing_obj = self.insert_user_fields(existing_obj, authorized, type="update")
        for k, v in obj.dict(exclude_unset=True).items():
            if v is not None:
                setattr(existing_obj, k, v)

        self.context.db_session.add(existing_obj)
        await self.context.db_session.commit()
        await self.context.db_session.refresh(existing_obj)

        return existing_obj

class PipelineConfigService(BaseService):
    model: PipelineConfig = PipelineConfig
    create_model: PipelineConfigCreate = PipelineConfigCreate
    update_model: PipelineConfigUpdate = PipelineConfigUpdate
    return_schema: PipelineConfigReturn = PipelineConfigReturn

class PipelineVersionService(BaseService):
    model: PipelineVersion = PipelineVersion
    create_model: PipelineVersionCreate = PipelineVersionCreate
    update_model: PipelineVersionUpdate = PipelineVersionUpdate
    return_schema: PipelineVersionReturn = PipelineVersionReturn


class PipelineDebugService:
    def __init__(self, host='host.docker.internal', port=15003):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.operations_stub = pipeline_operations_pb2_grpc.PipelineOperationsServiceStub(self.channel)
        self.data_stub = data_pb2_grpc.DataServiceStub(self.channel)

    async def start_pipeline(self, pipeline_name, pipeline_json, mode, checkpoints=None):
        # submit the pipeline
        request = pipeline_operations_pb2.StartPipelineRequest(
            pipeline_name=pipeline_name,
            pipeline_json=pipeline_json,
            mode=mode,
            checkpoints=checkpoints,
        )
        response = MessageToDict(self.operations_stub.StartPipeline(request))
        return response.get('message')

    async def stop_pipeline(self, pipeline_name):
        request = pipeline_operations_pb2.StopPipelineRequest(
            pipeline_name=pipeline_name
        )
        response = MessageToDict(self.operations_stub.StopPipeline(request))
        return response.get('message')

    async def get_transformation_output(self, pipeline_name, transformation_name, page, page_size, sort_columns):
        request = data_pb2.TransformationRequest(
            pipeline_name=pipeline_name,
            transformation_name=transformation_name,
            page=page,
            page_size=page_size,
            sort_columns=[data_pb2.SortColumn(name=col, order='asc') for col in sort_columns]
        )
        response = MessageToDict(self.data_stub.GetTransformationOutput(request))

        # Transform the response to the desired format
        for output in response.get('outputs', []):
            output['rows'] = [row['data'] for row in output.get('rows', [])]

        return response

    async def get_transformation_count(self, pipeline_name):
        request = data_pb2.GetTransformationOutputCountsRequest(
            pipeline_name=pipeline_name
        )
        response = MessageToDict(self.data_stub.GetTransformationOutputCounts(request))
        return response

    async def run_next_checkpoint(self, pipeline_name):
        request = pipeline_operations_pb2.NextCheckpointRequest(
            pipeline_name=pipeline_name
        )
        response = MessageToDict(self.operations_stub.NextCheckpoint(request))
        return response.get('message')


class PipelineLogService:
    def __init__(self, host='host.docker.internal', port=15003):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')
        self.log_stub = log_pb2_grpc.LogServiceStub(self.channel)

    async def stream_logs(self, pipeline_name: str):
        request = log_pb2.LogRequest(pipeline_name=pipeline_name)
        async for response in self.log_stub.StreamLogs(request):
            yield response.log_line


class PipelineConnectionService(BaseService):
    model: PipelineConnection = PipelineConnection
    create_model: PipelineConnectionCreate = PipelineConnectionCreate
    update_model: PipelineConnectionUpdate = PipelineConnectionUpdate
    return_schema: PipelineConnectionReturn = PipelineConnectionReturn


class PipelineParameterService(BaseService):
    model: PipelineParameter = PipelineParameter
    create_model: PipelineParameterCreate = PipelineParameterCreate
    update_model: PipelineParameterUpdate = PipelineParameterUpdate
    return_schema: PipelineParameterReturn = PipelineParameterReturn

    async def get_pipeline_parameters(self, pipeline_id: int):
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        return result.scalars().all()

    async def get_pipeline_parameters_by_type(self, pipeline_id: int, parameter_type: ParameterType):
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, self.model.parameter_type == parameter_type, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        return result.scalars().all()
    
    async def get_pipeline_parameters_by_pipeline_name(self, pipeline_name: str):
        statement = select(PipelineParameter).join(Pipeline).filter(Pipeline.pipeline_name == pipeline_name, or_(PipelineParameter.is_deleted == False, PipelineParameter.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        return result.scalars().all()
    
    async def get_pipeline_parameter_by_name(self, pipeline_id: int, parameter_name: str):
        statement = select(self.model).where(self.model.pipeline_id == pipeline_id, self.model.parameter_name == parameter_name, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        pipeline_parameter = result.scalar_one_or_none()

        if not pipeline_parameter:
            raise ObjectNotFound(context={
                'column_name': 'parameter_name',
                'value': parameter_name,
                'type': 'PipelineParameter',
            })
        
        return pipeline_parameter
