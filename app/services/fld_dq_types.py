from app.models.fld_dq_types import (
    FieldDQTypes,
    FieldDQTypesCreate,
    FieldDQTypesUpdate,
    FieldDQReturn,
)

from app.services.base import BaseService

class FieldDQTypesService(BaseService):
    model: FieldDQTypes = FieldDQTypes
    create_model: FieldDQTypesCreate = FieldDQTypesCreate
    update_model: FieldDQTypesUpdate = FieldDQTypesUpdate
    return_schema: FieldDQReturn = FieldDQReturn