from app.models.layout_fields_dq import (
    LayoutFieldsDQ,
    LayoutFieldsDQCreate,
    LayoutFieldsDQUpdate,
    LayoutFieldsDQReturn,
)

from app.services.base import BaseService


class LayoutFieldsDQService(BaseService):
    model = LayoutFieldsDQ
    create_model = LayoutFieldsDQCreate
    update_model = LayoutFieldsDQUpdate
    return_schema = LayoutFieldsDQReturn
