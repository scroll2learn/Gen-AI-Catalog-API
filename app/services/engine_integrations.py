from app.services.base import BaseService

from sqlalchemy import select

from app.models import (
    BHProject,
    LakeZone,
    DataSource,
    DataSourceLayout,
    LayoutFields,
    LayoutFieldsDQ,
    Pipeline,
)

model_to_export = {
    "bh_project": BHProject,
    "lake_zone": LakeZone,
    "data_source": DataSource,
    "data_source_layout": DataSourceLayout,
    "layout_fields": LayoutFields,
    "layout_fields_dq": LayoutFieldsDQ,
    "pipelines": Pipeline,
}


class EngineConfigurationsService(BaseService):

    async def export_tables(self, models_to_export=model_to_export):
        engine_config = {}
        for model in models_to_export:
            self.model = models_to_export.get(model)
            stmt = select(self.model)
            response = await self.context.db_session.execute(stmt)
            engine_config[model] = response.scalars().all()
        
        return engine_config

    async def _get_cd_id_to_desc(self, id):
        code_object = await self.context.codes_dtl_service.get(id=id)
        code_dict = code_object.dict()
        return code_dict['dtl_desc']

    async def _convert_cd_to_value(self, cd_dict):
        new_cd_dict = cd_dict.copy()
        for key in cd_dict.keys():
            if '_cd' in key:
                code_value = await self._get_cd_id_to_desc(id=cd_dict[key])
                new_key = key.replace('_cd', '_val')    
                new_cd_dict[new_key] = code_value
        return new_cd_dict

    async def engine_config_export(
            self, 
            data_source_id = None,
            data_source_name = None,
            data_source_key = None,
        ):
        engine_config = {}
        data_source = await self.context.data_source_service.get(id=data_source_id)
        engine_config['data_source'] = data_source.dict()
        engine_config['data_source'] = await self._convert_cd_to_value(engine_config['data_source'])
        data_source_layouts = await self.context.data_source_layout_service.list(data_src_id=data_source_id)
        layouts_list = []
        for layout in data_source_layouts:
            layout_dict = layout.dict()
            layout_dict = await self._convert_cd_to_value(layout_dict)
            layout_fields = await self.context.layout_fields_service.list(lyt_id=layout.data_src_lyt_id)
            layout_fields_list = []
            for lyt_field in layout_fields:
                lyt_field_dict = lyt_field.dict()
                lyt_field_dict = await self._convert_cd_to_value(lyt_field_dict)
                lyt_field_validations = await self.context.layout_fields_dq_service.list(lyt_fld_id=lyt_field.lyt_fld_id)
                validation_list = []
                for validation in lyt_field_validations:
                    validation_dict = validation.dict()
                    dq_response  = await self.context.fields_dq_types_service.get(id=validation_dict['fld_dq_type_id'])
                    validation_dict['dq_name'] = dq_response.dq_name
                    validation_list.append(validation_dict)
                lyt_field_dict['field_validations'] = validation_list
                layout_fields_list.append(lyt_field_dict)
            layout_dict['layout_fields'] = layout_fields_list
            layouts_list.append(layout_dict)
        engine_config['data_source_layout'] = layouts_list
        return engine_config
