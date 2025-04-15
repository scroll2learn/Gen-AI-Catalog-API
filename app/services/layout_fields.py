from app.models.layout_fields import (
    LayoutFields,
    LayoutFieldsCreate,
    LayoutFieldsUpdate,
    LayoutFieldsReturn,
    LayoutDescriptionUpdate,
)
from app.services.base import BaseService
from typing import List


class LayoutFieldsService(BaseService):
    model: LayoutFields = LayoutFields
    create_model: LayoutFieldsCreate = LayoutFieldsCreate
    update_model: LayoutFieldsUpdate = LayoutFieldsUpdate
    return_schema: LayoutFieldsReturn = LayoutFieldsReturn
    name_field: str = 'lyt_fld_name'
    key_field: str = 'lyt_fld_key'

    async def create_bulk_fields(self, layout_fields_list: List[LayoutFieldsCreate]) -> List[LayoutFieldsReturn]:
        new_list = [self.model.from_orm(obj) for obj in layout_fields_list]
        self.context.db_session.add_all(new_list)
        await self.context.db_session.commit()
        for obj in new_list:
            await self.context.db_session.refresh(obj)
        return new_list

    async def update_fields_pk(self, field_ids: List, is_pk: bool):
        for field_id in field_ids:
            existing_obj = await self.get(id=field_id)
            setattr(existing_obj, 'lyt_fld_is_pk', is_pk)

            self.context.db_session.add(existing_obj)
            await self.context.db_session.commit()
            await self.context.db_session.refresh(existing_obj)

    async def update_bulk_descriptions(self, lyt_id: int, descriptions: List[LayoutDescriptionUpdate]):
        for desc in descriptions:
            existing_obj = await self.get(id=desc.lyt_fld_id)
            
            # Verify the field belongs to the specified layout
            if existing_obj.lyt_id != lyt_id:
                raise ValueError(f"Field {desc.lyt_fld_id} does not belong to layout {lyt_id}")
                
            setattr(existing_obj, 'lyt_fld_desc', desc.lyt_fld_desc)
            self.context.db_session.add(existing_obj)
        
        await self.context.db_session.commit()
