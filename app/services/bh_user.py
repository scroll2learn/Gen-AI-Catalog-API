from typing import Optional, List
from sqlalchemy import delete, select, desc
from sqlalchemy.future import select
from app.exceptions import ObjectNotFound

from app.models.bh_user import (
    BHUser,
    BHUserCreate,
    BHUserUpdate,
    BHUserReturn
)

from app.models.base import (
    UserDetail,
    UserDetailBase,
    UserDetailReturn
)
from app.services.base import BaseService


class BHUserService(BaseService):
    model: BHUser = BHUser
    create_model: BHUserCreate = BHUserCreate
    update_model: BHUserUpdate = BHUserUpdate
    return_schema: BHUserReturn = BHUserReturn

class UserDetailService(BaseService):
    model: UserDetail = UserDetail
    create_model: UserDetailBase = UserDetailBase
    update_model: UserDetailBase = UserDetailBase
    return_schema: UserDetailReturn = UserDetailReturn

    async def list(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_schema]:
        query = select(self.model)
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
    
    async def get(self, id: int):
        primary_key_column = await self._get_primary_key_column()
        statement = select(self.model).filter(primary_key_column == id)
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()

        if response is None:
            raise ObjectNotFound(context={
                'column_name': primary_key_column.name,
                'id': id,
                'type': self.model.__name__,
            })

        return response
    
    async def update(self, id: int, obj: update_model):
        existing_obj = await self.get(id=id)
        for k, v in obj:
            if v is not None:
                setattr(existing_obj, k, v)

        self.context.db_session.add(existing_obj)
        await self.context.db_session.commit()
        await self.context.db_session.refresh(existing_obj)

        return existing_obj
    
    async def delete(self, id: int, authorized: dict = None):
        """Soft delete the apis. Set is_deleted = True and update deleted_by in db"""

        primary_key_column = await self._get_primary_key_column()
        statement = delete(
                    self.model
                ).where(
                    primary_key_column == id
                )

        await self.context.db_session.execute(statement=statement)
        await self.context.db_session.commit()

        return True
    
    async def get_or_create_user_detail(
        self,
        username: str, 
        email: str
    ) -> UserDetail:
        
        # Check if a user with the same username or user_id exists
        query = select(UserDetail).where((UserDetail.username == username))
        result = await self.context.db_session.execute(query)
        existing_user = result.scalars().first()
        
        # If user exists, return the existing user details
        if existing_user:
            return existing_user
        
        # Otherwise, create a new user using the BaseService `create` method
        new_user_data = UserDetailBase(username=username, user_email=email)
        new_user = await self.create(new_user_data)
        
        return new_user