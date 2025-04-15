from typing import Dict, Type, TypeVar

from pydantic import BaseModel
from typing_extensions import Literal

from app.db.base_class import Base

OrderBy = Dict[str, Literal['asc', 'desc']]

ModelType = TypeVar('ModelType', bound=Base)
Model = Type[ModelType]

SchemaType = TypeVar('SchemaType', bound=BaseModel)
Schema = Type[SchemaType]