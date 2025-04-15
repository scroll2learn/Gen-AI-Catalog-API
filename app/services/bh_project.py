
from typing import List, Optional
from app.exceptions.base import ObjectNotFound
from app.models.bh_project import (
    BHProject,
    BHProjectCreate,
    BHProjectUpdate,
    BHProjectReturn,
    LakeZone,
    LakeZoneCreate,
    LakeZoneUpdate,
    LakeZoneReturn,
    PreConfigureZone,
    PreConfigureZoneCreate,
    PreConfigureZoneReturn,
    PreConfigureZoneUpdate,
    ProjectEnvironment,
    ProjectEnvironmentCreate,
    ProjectEnvironmentUpdate,
    ProjectEnvironmentReturn,
    ConfigureLifecycle,
    ConfigureLifecycleCreate,
    ConfigureLifecycleUpdate,
    ConfigureLifecycleReturn,
    FlowConnection,
    FlowConnectionCreate,
    FlowConnectionReturn,
    FlowConnectionUpdate
)
from app.models.codes_hdr import CodesDtl
from app.models.data_source import DataSource
from app.services.base import BaseService
from sqlalchemy.orm import aliased
from sqlalchemy import or_, select, func, desc

class BHProjectService(BaseService):
    model: BHProject = BHProject
    create_model: BHProjectCreate = BHProjectCreate
    update_model: BHProjectUpdate = BHProjectUpdate
    return_schema: BHProjectReturn = BHProjectReturn

    async def check_project_exists(
        self,
        bh_project_name: str = None,
    ):
        statement = select(self.model).where(self.model.bh_project_name == bh_project_name, or_(self.model.is_deleted == False, self.model.is_deleted == None))
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
    ) -> List[return_schema]:
        
        query = select(self.model, func.count(DataSource.data_src_id).label('total_data_sources')).\
                join(DataSource, self.model.bh_project_id == DataSource.bh_project_id, isouter=True).\
                group_by(self.model.bh_project_id).where(or_(self.model.is_deleted == False))

        for kw in kwargs.keys():
            if kwargs[kw] is not None:
                query = query.where(getattr(self.model, kw) == kwargs[kw])

        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        query = query.offset(offset).limit(limit)

        results = await self.context.db_session.execute(query)

        return [
            self.return_schema(
                **project.__dict__,  
                total_data_sources=count  # Add the data source count
            )
            for project, count in results.all()
        ]
    
    async def get_by_id(self, bh_project_id: int) -> Optional[return_schema]:
        """
        Fetch a BHProject by its ID.
        :param bh_project_id: ID of the BHProject.
        :return: BHProjectReturn schema or None if not found.
        """
        statement = select(self.model).where(self.model.bh_project_id == bh_project_id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement)
        project = result.scalar_one_or_none()
        if project:
            return self.return_schema.from_orm(project)
        return None

class LakeZoneService(BaseService):
    model: LakeZone = LakeZone
    create_model: LakeZoneCreate = LakeZoneCreate
    update_model: LakeZoneUpdate = LakeZoneUpdate
    return_schema: LakeZoneReturn = LakeZoneReturn

class ProjectEnvironmentService(BaseService):
    model: ProjectEnvironment = ProjectEnvironment
    create_model: ProjectEnvironmentCreate = ProjectEnvironmentCreate
    update_model: ProjectEnvironmentUpdate = ProjectEnvironmentUpdate
    return_schema: ProjectEnvironmentReturn = ProjectEnvironmentReturn

    async def list(
        self,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        **kwargs,
    ) -> List[return_schema]:
        
        # Create aliases for the CodesDtl table for bh_env_provider and cloud_provider_cd
        bh_env_provider_alias = aliased(CodesDtl)
        cloud_provider_alias = aliased(CodesDtl)

        query = (
            select(self.model, bh_env_provider_alias, cloud_provider_alias)
            .outerjoin(bh_env_provider_alias, self.model.bh_env_provider == bh_env_provider_alias.id)  # Join for bh_env_provider with alias
            .outerjoin(cloud_provider_alias, self.model.cloud_provider_cd == cloud_provider_alias.id)  # Join for cloud_provider_cd with alias
            .where(or_(self.model.is_deleted == False, self.model.is_deleted == None))
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

        # Iterate over the results and process the tuple (ProjectEnvironment, bh_env_provider_alias, cloud_provider_alias)
        result_list = []
        for result in results:
            project_environment = result[0]  
            bh_env_provider = result[1]  
            cloud_provider = result[2] 

            result_list.append(self.return_schema.from_orm_with_aliases(
                project_environment, 
                bh_env_provider, 
                cloud_provider
            ))

        return result_list
    
    async def get_env(self, id: int):
        # Create aliases for the CodesDtl table for bh_env_provider and cloud_provider_cd
        bh_env_provider_alias = aliased(CodesDtl)
        cloud_provider_alias = aliased(CodesDtl)

        primary_key_column = await self._get_primary_key_column()

        # Modified query with table aliases for joins
        statement = (
            select(self.model, bh_env_provider_alias, cloud_provider_alias)
            .outerjoin(bh_env_provider_alias, self.model.bh_env_provider == bh_env_provider_alias.id)  # Join for bh_env_provider
            .outerjoin(cloud_provider_alias, self.model.cloud_provider_cd == cloud_provider_alias.id)  # Join for cloud_provider_cd
            .filter(primary_key_column == id, or_(self.model.is_deleted == False, self.model.is_deleted == None))
        )

        result = await self.context.db_session.execute(statement=statement)
        response = result.first() 

        if response is None:
            raise ObjectNotFound(context={
                'column_name': primary_key_column.name,
                'id': id,
                'type': self.model.__name__,
            })

        project_environment = response[0]  
        if not isinstance(project_environment, self.model):
            raise ValueError("Project environment instance is not mapped.")

        bh_env_provider = response[1]  # bh_env_provider_alias object
        cloud_provider = response[2]  # cloud_provider_alias object

        # Return the response using the from_orm_with_aliases method
        return self.return_schema.from_orm_with_aliases(
            project_environment, 
            bh_env_provider, 
            cloud_provider
        )
    
    async def update_env(self, id: int, obj: update_model):
        existing_obj = await self.get(id=id)
        for k, v in obj:
            if v is not None:
                setattr(existing_obj, k, v)

        self.context.db_session.add(existing_obj)
        await self.context.db_session.commit()
        await self.context.db_session.refresh(existing_obj)

        return existing_obj

    

class PreConfigureZoneService(BaseService):
    model: PreConfigureZone = PreConfigureZone
    create_model: PreConfigureZoneCreate = PreConfigureZoneCreate
    update_model: PreConfigureZoneUpdate = PreConfigureZoneUpdate
    return_schema: PreConfigureZoneReturn = PreConfigureZoneReturn

class ConfigureLifecycleService(BaseService):
    model: ConfigureLifecycle = ConfigureLifecycle
    create_model: ConfigureLifecycleCreate = ConfigureLifecycleCreate
    update_model: ConfigureLifecycleUpdate = ConfigureLifecycleUpdate
    return_schema: ConfigureLifecycleReturn = ConfigureLifecycleReturn

class FlowConnectionService(BaseService):
    model: FlowConnection = FlowConnection
    create_model: FlowConnectionCreate = FlowConnectionCreate
    update_model: FlowConnectionUpdate = FlowConnectionUpdate
    return_schema: FlowConnectionReturn = FlowConnectionReturn