from app.models.transform_logic import (
    TransformLogic,
    TransformLogicCreate,
    TransformLogicUpdate,
    TransformLogicReturn,
    TransformInputFields,
    TransformInputFieldsCreate,
    TransformInputFieldsUpdate,
    TransformInputFieldsReturn,
    TransformOutputFields,
    TransformOutputFieldsCreate,
    TransformOutputFieldsUpdate,
    TransformOutputFieldsReturn,
)

from app.services.base import BaseService


class TransformLogicService(BaseService):
    model: TransformLogic = TransformLogic
    create_model: TransformLogicCreate = TransformLogicCreate
    update_model: TransformLogicUpdate = TransformLogicUpdate
    return_schema: TransformLogicReturn = TransformLogicReturn


class TransformInputFieldsService(BaseService):
    model: TransformInputFields = TransformInputFields
    create_model: TransformInputFieldsCreate = TransformInputFieldsCreate
    update_model: TransformInputFieldsUpdate = TransformInputFieldsUpdate
    return_schema: TransformInputFieldsReturn = TransformInputFieldsReturn


class TransformOutputFieldsService(BaseService):
    model: TransformOutputFields = TransformOutputFields
    create_model: TransformOutputFieldsCreate = TransformOutputFieldsCreate
    update_model: TransformOutputFieldsUpdate = TransformOutputFieldsUpdate
    return_schema: TransformOutputFieldsReturn = TransformOutputFieldsReturn
