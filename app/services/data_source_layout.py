
from app.models.data_source_layout import (
    DataSourceLayout,
    DataSourceLayoutCreate,
    DataSourceLayoutUpdate,
    DataSourceLayoutReturn,
    DataSourceLayoutFullReturn,
)
from app.services.base import BaseService
from app.exceptions import InvalidRegexProvided


class DataSourceLayoutService(BaseService):
    model: DataSourceLayout = DataSourceLayout
    create_model: DataSourceLayoutCreate = DataSourceLayoutCreate
    update_model: DataSourceLayoutUpdate = DataSourceLayoutUpdate
    return_schema: DataSourceLayoutReturn = DataSourceLayoutReturn
    return_full_schema: DataSourceLayoutFullReturn = DataSourceLayoutFullReturn
    name_field: str = 'data_src_lyt_name'
    key_field: str = 'data_src_lyt_key'

    def update_layout(
            self,
            data_src_lyt_id: int,
            layout_object: DataSourceLayoutUpdate,
            authorized: dict = None
    ) -> DataSourceLayoutReturn:
        import re
        if layout_object.data_src_lyt_regex:
            try:
                re.compile(layout_object.data_src_lyt_regex)
            except Exception as e:
                raise InvalidRegexProvided
        return self.update(data_src_lyt_id, layout_object, authorized=authorized)
