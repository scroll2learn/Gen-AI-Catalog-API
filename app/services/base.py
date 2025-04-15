import re

from abc import ABC

from app.exceptions.base import CreateException
from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder
from app.types import ModelType, SchemaType
from sqlalchemy import delete, select, desc, or_, cast, String
from sqlalchemy.types import BOOLEAN, INTEGER
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance
from sqlalchemy import inspect

from typing import Optional, List, Dict
from app.core.context import Context
from app.exceptions import ObjectNotFound
from datetime import datetime

class BaseService(ABC):
    model: ModelType = None
    create_model: ModelType = None
    update_model: ModelType = None
    return_schema: SchemaType = None
    return_full_schema: SchemaType = None
    name_field: str = None
    key_field: str = None

    def __init__(self, context: Context):
        self.context: Context = context

    async def _get_primary_key_column(self):
        # Inspect the model to find the primary key column
        primary_key_columns = inspect(self.model).primary_key
        if not primary_key_columns:
            raise ValueError(f"No primary key found for model {self.model.__name__}")
        # Assuming single-column primary key; adjust if your models use composite primary keys
        return primary_key_columns[0]

    def name_to_key_parser(self, name: str) -> str:
        """ To replace any special characters with underscore in field name
            and only allow alphanumeric characters & underscore.
        Args:
            field_name: str: Field Name"""
        name = re.sub('[^a-zA-Z0-9]', '_', name).lower()
        return name

    async def list_full(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_full_schema]:
        
        query = select(self.model)

        # To provide filter on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit).where(or_(self.model.is_deleted == False, self.model.is_deleted == None))
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        return [self.return_full_schema.from_orm(result) for result in results.scalars()]

    async def list(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_schema]:
        
        query = select(self.model).where(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        # To provide filter on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        return [self.return_schema.from_orm(result) for result in results.scalars()]
    
    async def search(self, params: Dict[str, str]) -> List[return_schema]:
        query = select(self.model).filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))
        for field, search_key in params.items():
            model_field = getattr(self.model, field)
            if type(model_field) is ColumnAssociationProxyInstance:
                #join the associated column using the local relationship
                query = query.join(model_field.target_class, model_field.local_attr)
                model_field = model_field.remote_attr
            if model_field.type == INTEGER:
                query = query.filter(or_(*[model_field == int(key) for key in search_key]))
            elif model_field.type == BOOLEAN:
                if str(search_key[0]).lower() == 'true':
                    query = query.filter(model_field.is_(True))
                elif str(search_key[0]).lower() == 'false':
                    query = query.filter(model_field.is_(False))
            else:
                # Cast as String in case of JSON
                query = query.filter(or_(*[cast(model_field, String).ilike(f'%{key}%') for key in search_key]))

        results = await self.context.db_session.exec(query)

        return [self.return_schema.from_orm(result) for result in results.scalars()]
    

    def insert_user_fields(
        self,
        obj: model, 
        authorized: Optional[dict] = None, 
        type: str = None
    ) -> model:
        """Insert `created_by`, `updated_by` and `updated_by` fields into the model object."""
        if hasattr(obj, "created_by") and authorized and "user_detail_id" in authorized and type == "create":
            obj.created_by = authorized["user_detail_id"]
        if hasattr(obj, "updated_by") and authorized and "user_detail_id" in authorized and type == "update":
            obj.updated_by = authorized["user_detail_id"]
            obj.updated_at = datetime.now()
        if hasattr(obj, "deleted_by") and authorized and "user_detail_id" in authorized and type == "delete":
            obj.deleted_by = authorized["user_detail_id"]
            obj.is_deleted = True
        return obj

    async def create(self, obj: create_model, authorized: dict = None):
        new_obj = self.model.from_orm(obj)
        if authorized:
            new_obj = self.insert_user_fields(new_obj, authorized, type="create")
        if self.name_field and self.key_field:
            setattr(new_obj, self.key_field, (self.name_to_key_parser(new_obj.__dict__[self.name_field])))
        try:
            self.context.db_session.add(new_obj)
            await self.context.db_session.commit()
            await self.context.db_session.refresh(new_obj)
        except Exception as e:
            print('------Exception-----')
            print(e)
            raise CreateException(
                context={
                    'error': str(e),
                }
            )
        return new_obj
    
    async def get(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        statement = select(self.model).filter(primary_key_column == id)
        if hasattr(self.model, "is_deleted"):
            statement = statement.filter(or_(self.model.is_deleted == False, self.model.is_deleted == None))
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()

        if response is None:
            raise ObjectNotFound(context={
                'column_name': primary_key_column.name,
                'id': id,
                'type': self.model.__name__,
            })

        return response


    async def update(self, id: int, obj: update_model, authorized: dict = None):
        existing_obj = await self.get(id=id)
        if authorized:
            existing_obj = self.insert_user_fields(existing_obj, authorized, type="update")
        for k, v in obj:
            if v is not None:
                setattr(existing_obj, k, v)

        self.context.db_session.add(existing_obj)
        await self.context.db_session.commit()
        await self.context.db_session.refresh(existing_obj)

        return existing_obj

    async def model_update(self, id: int, obj: update_model, avoid: list = []):
        existing_obj = await self.get(id=id)
        
        old_value = await self.encode(existing_obj)
        
        for k, v in obj.dict(exclude_unset=True).items():
            if (k not in avoid) and (v is not None):
                setattr(existing_obj, k, v)

        self.context.db_session.add(existing_obj)
        await self.context.db_session.commit()
        await self.context.db_session.refresh(existing_obj)

        return existing_obj


    async def delete(self, id: int, authorized: dict = None):
        """Soft delete the apis. Set is_deleted = True and update deleted_by in db"""
        existing_obj = await self.get(id=id)
        if authorized:
            existing_obj = self.insert_user_fields(existing_obj, authorized, type="delete")

        await self.update(id=id, obj=existing_obj)
        # primary_key_column = await self._get_primary_key_column()
        # statement = delete(
        #             self.model
        #         ).where(
        #             primary_key_column == id
        #         )

        # await self.context.db_session.execute(statement=statement)
        # await self.context.db_session.commit()

        return True

    async def encode(self, object: object) -> dict:
        try:
            json_object = jsonable_encoder(object)
        except RecursionError:
            json_object = jsonable_encoder(self.return_schema.from_orm(object))
        return json_object