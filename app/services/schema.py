from app.enums.flow import SchemaTypes
from app.exceptions.base import ObjectNotFound
from app.models.schema import (
    Schema,
    SchemaCreate,
    SchemaUpdate,
    SchemaReturn
)
from app.services.base import BaseService
from sqlalchemy import select, func

class SchemaService(BaseService):
    model: Schema = Schema
    create_model: SchemaCreate = SchemaCreate
    update_model: SchemaUpdate = SchemaUpdate
    return_schema: SchemaReturn = SchemaReturn

    async def get_latest_by_type(self, schema_type: SchemaTypes):
        
        statement = (
            select(func.max(self.model.schema_id))
            .where(self.model.schema_type == schema_type)
        )
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()

        if response is None:
            raise ObjectNotFound(context={
                'schema_type': schema_type,
                'type': self.model.__name__,
            })

        return response
