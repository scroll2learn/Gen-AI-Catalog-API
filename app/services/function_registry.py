from app.models.function_registry import (
    FunctionRegistry,
    FunctionRegistryCreate,
    FunctionRegistryUpdate,
    FunctionRegistryReturn,
)

from app.services.base import BaseService


class FunctionRegistryService(BaseService):
    model = FunctionRegistry
    create_schema = FunctionRegistryCreate
    update_schema = FunctionRegistryUpdate
    return_schema = FunctionRegistryReturn
    name_field: str = 'function_name'
    key_field: str = 'function_key'
