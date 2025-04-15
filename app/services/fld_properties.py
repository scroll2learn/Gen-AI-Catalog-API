from app.models.fld_properties import (
    FieldProperties,
    FieldPropertiesCreate,
    FieldPropertiesUpdate,
    FieldPropertiesReturn,
)

from app.services.base import BaseService
from typing import List

from app.exceptions import ObjectNotFound

class FieldPropertiesService(BaseService):
    model: FieldProperties = FieldProperties
    create_model: FieldPropertiesCreate = FieldPropertiesCreate
    update_model: FieldPropertiesUpdate = FieldPropertiesUpdate
    return_schema: FieldPropertiesReturn = FieldPropertiesReturn


    async def create_or_update_field_properties(
            self,
            flds_properties_list: List[FieldPropertiesCreate]
            ) -> List[FieldPropertiesReturn]:
        new_list = [self.model.from_orm(obj) for obj in flds_properties_list]
        update_lsit = []
        for obj in new_list:
            try:
                get_response = await self.get(id=obj.fld_id)
            except ObjectNotFound:
                get_response = None
            if get_response:
                update_lsit.append(obj.dict())
                new_list.remove(obj)
                for k, v in obj:
                    if v is not None:
                        setattr(get_response, k, v)
                self.context.db_session.add(get_response)
        self.context.db_session.add_all(new_list)
        await self.context.db_session.commit()
        for obj in new_list:
            await self.context.db_session.refresh(obj)
        return new_list
