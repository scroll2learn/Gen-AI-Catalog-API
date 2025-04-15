import json
from app.exceptions.base import ObjectNotFound
from app.models.bh_project import BHProject
from app.models.flow import (
    Flow,
    FlowCreate,
    FlowUpdate,
    FlowReturn,
    FlowDeployment,
    FlowDeploymentCreate,
    FlowDeploymentUpdate,
    FlowDeploymentReturn,
    FlowDefinition,
    FlowDefinitionCreate,
    FlowDefinitionUpdate,
    FlowDefinitionReturn,
    FlowVersion,
    FlowVersionCreate,
    FlowVersionUpdate,
    FlowVersionReturn,
    FlowConfig,
    FlowConfigCreate,
    FlowConfigUpdate,
    FlowConfigReturn
)
from app.services.base import BaseService
from app.utils.flow_utils import create_flow_release_version
from app.utils.git_utils.git_utils import create_git_branch, initialize_git_provider
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import or_, select, desc, delete
from typing import Optional, List , Dict
from sqlalchemy.future import select
from sqlalchemy.types import BOOLEAN, INTEGER
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance


class FlowService(BaseService):
    model: Flow = Flow
    create_model: FlowCreate = FlowCreate
    update_model: FlowUpdate = FlowUpdate
    return_schema: FlowReturn = FlowReturn

    async def list(
        self,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        **kwargs,
    ) -> List[return_schema]:
        query = (
            select(self.model)
            .where(or_(self.model.is_deleted == False, self.model.is_deleted == None))
            .options(
                joinedload(self.model.bh_project),
                joinedload(self.model.flow_deployment).joinedload(FlowDeployment.project_environment),
                joinedload(self.model.created_by_user),  
                joinedload(self.model.updated_by_user),   
            )
        )

        for kw in kwargs.keys():
            if kwargs[kw] is not None:
                query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)
        
        results = await self.context.db_session.execute(query)

        unique_results = results.unique().scalars()

        return [
            self.return_schema.from_orm(result).copy(
                update={
                    "bh_project_name": result.bh_project.bh_project_name,
                    "flow_deployment": [
                        FlowDeploymentReturn.from_orm(deployment).copy(
                            update={"bh_env_name": deployment.project_environment.bh_env_name}
                        )
                        for deployment in result.flow_deployment
                    ],
                "created_by_username": result.created_by_user.username if result.created_by_user else None,
                "updated_by_username": result.updated_by_user.username if result.updated_by_user else None,
                }
            )
            for result in unique_results
        ]


    async def search(self, params: Dict[str, str]) -> List[return_schema]:
        query = select(self.model).filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        for field, search_key in params.items():
            model_field = getattr(self.model, field) 

            if type(model_field) is ColumnAssociationProxyInstance:
                # Join the associated column using the local relationship
                query = query.join(model_field.target_class, model_field.local_attr)
                model_field = model_field.remote_attr

            if model_field.type == INTEGER:
                # Filter for exact match for integers
                query = query.filter(model_field.in_([int(key) for key in search_key]))
            elif model_field.type == BOOLEAN:
                # Filter for exact match for booleans
                if str(search_key[0]).lower() == 'true':
                    query = query.filter(model_field.is_(True))
                elif str(search_key[0]).lower() == 'false':
                    query = query.filter(model_field.is_(False))
            else:
                # Exact match for strings
                query = query.filter(model_field.in_(search_key))

        results = await self.context.db_session.exec(query)
        return [self.return_schema.from_orm(result) for result in results.scalars()]


    async def check_flow_exists(
        self,
        flow_name: str = None,
    ):
        statement = select(self.model).where(self.model.flow_name == flow_name, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()
        return response

    
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

    async def get_flow(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        
        # Modify the select query to load both schedule_interval and flow_deployment relationships
        statement = (
            select(self.model)
            .filter(primary_key_column == id)
            .options(
                selectinload(self.model.flow_deployment)
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
        
        query = select(self.model).where(self.model.flow_id == id)
        if not include_deleted:
            query = query.where(or_(self.model.is_deleted == False, self.model.is_deleted == None))  # Exclude soft-deleted
        result = await self.context.db_session.execute(query)
        return result.scalar_one_or_none()



    
class FlowDeploymentService(BaseService):
    model: FlowDeployment = FlowDeployment
    create_model: FlowDeploymentCreate = FlowDeploymentCreate
    update_model: FlowDeploymentUpdate = FlowDeploymentUpdate
    return_schema: FlowDeploymentReturn = FlowDeploymentReturn

    async def get_flow_deployment_with_flow(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        statement = (
            select(self.model)
                .filter(primary_key_column == id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
                .options(
                    joinedload(self.model.flow).joinedload(Flow.bh_project),  
                    joinedload(self.model.flow).joinedload(Flow.flow_definition),  
                    joinedload(self.model.project_environment), 
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

    async def create_commit(
            self,
            flow: Flow,
            project: BHProject,
            branch: Optional[str] = None,
            commit: str = "Pipeline Commit",
            flow_json: Optional[str] = None,
            github_token: Optional[str] = None,
            dag_file: Optional[str] = None) -> dict:
        git_provider = await initialize_git_provider(project, github_token)
        await create_git_branch(git_provider, branch)
        
        files_to_commit = {
            f"flow/{flow.flow_id}/schema/flows.json": json.dumps(flow_json or {}),
        }
        if dag_file:
            files_to_commit[f"flow/{flow.flow_id}/dag/dag_file.py"] = dag_file

        # Commit the files 
        commit_result = await git_provider.commit_multiple_files(files_to_commit, commit, branch)

        return commit_result

    async def list(
        self,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        **kwargs,
    ) -> List[return_schema]:
        
        # Join the Flow table to retrieve flow_name
        query = select(self.model).options(joinedload(self.model.flow), joinedload(self.model.project_environment)).filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        for kw in kwargs.keys():
            if kwargs[kw] is not None:
                query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        # Iterate over results, and manually map them to the return schema
        return [
            self.return_schema(
                **vars(result),  
                flow_name=result.flow.flow_name if result.flow else None,
                bh_env_name=result.project_environment.bh_env_name if result.project_environment else None
            )
            for result in results.scalars()
        ]


class FlowDefinitionService(BaseService):
    model: FlowDefinition = FlowDefinition
    create_model: FlowDefinitionCreate = FlowDefinitionCreate
    update_model: FlowDefinitionUpdate = FlowDefinitionUpdate
    return_schema: FlowDefinitionReturn = FlowDefinitionReturn

    async def get_flow_definition_by_flow_id(self, flow_id: int) -> FlowDefinition:
        """
        Retrieve FlowDefinition by flow_id.
        """
        statement = select(self.model).where(self.model.flow_id == flow_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        flow_definition = result.scalar_one_or_none()

        if not flow_definition:
            raise ObjectNotFound(context={
                'column_name': 'flow_id',
                'id': flow_id,
                'type': 'FlowDefinition',
            })

        return flow_definition

    async def delete_by_flow_id(self, flow_id: int, authorized: dict = None):
        """
        Delete FlowDefinition by flow_id.
        """
        
        statement = select(self.model).where(self.model.flow_id == flow_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        flow_definition = result.scalar_one_or_none()
        
        if not flow_definition:
            raise ObjectNotFound(context={
                'column_name': 'flow_id',
                'id': flow_id,
                'type': 'FlowDefinition',
            })
        if authorized:
            flow_definition = self.insert_user_fields(flow_definition, authorized, type="delete")
        await self.update(id=flow_definition.flow_definition_id, obj=flow_definition, authorized=authorized)

        return True
    
    async def update_by_flow_id(self, flow_id: int, obj: FlowDefinitionUpdate, authorized: dict = None):
        """
        Update FlowDefinition by flow_id.
        """
        statement = select(self.model).where(self.model.flow_id == flow_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        existing_obj = result.scalar_one_or_none()
        
        if not existing_obj:
            raise ObjectNotFound(context={
                'column_name': 'flow_id',
                'id': flow_id,
                'type': 'FlowDefinition',
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
    

class FlowVersionService(BaseService):
    model: FlowVersion = FlowVersion
    create_model: FlowVersionCreate = FlowVersionCreate
    update_model: FlowVersionUpdate = FlowVersionUpdate
    return_schema: FlowVersionReturn = FlowVersionReturn


class FlowConfigService(BaseService):
    model: FlowConfig = FlowConfig
    create_model: FlowConfigCreate = FlowConfigCreate
    update_model: FlowConfigUpdate = FlowConfigUpdate
    return_schema: FlowConfigReturn = FlowConfigReturn
