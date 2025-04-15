
from sqlalchemy.ext.declarative import as_declarative
from app.core.config import Config
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str
    __table_args__ = {"schema": Config.DB_SCHEMA}
