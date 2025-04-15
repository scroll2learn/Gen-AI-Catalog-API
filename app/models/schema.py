from sqlmodel import SQLModel, Field
from typing import Optional
from app.core.config import Config
from app.enums.flow import SchemaTypes
from app.models.base import TimestampModel

class SchemaBase(SQLModel):
    schema_id: int = Field(default=None, primary_key=True)
    schema_type: SchemaTypes = Field(..., description="Type of the schema, e.g., FLOW, PIPELINE, CONNECTIONS")
    commit_id: Optional[str] = Field(nullable=True, default=None, description="The commit identifier for the schema")
    version_tag: Optional[str] = Field(nullable=True, default=None, description="Version tag for the schema")
    comment: Optional[str] = Field(nullable=True, default=None, description="Comment or description of the schema")
    schema_path: Optional[str] = Field(nullable=True, default=None, description="Path to the schema file, e.g., Example schema/flows/flow.json")
    schema_dependencies_path: Optional[str] = Field(nullable=True, default=None, description="Path to the schema dependencies file, e.g., Example schema/flows/dependencies.json")
    platform_version: Optional[str] = Field(nullable=True, default=None, description="Platform version compatible with this schema")


class Schema(SchemaBase, TimestampModel, table=True):
    __tablename__ = "schema"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class SchemaCreate(SQLModel):
    schema_type: SchemaTypes = None
    commit_id: str = None
    version_tag: str = None
    comment: str = None
    schema_path: str = None
    schema_dependencies_path: str = None
    platform_version: str = None

class SchemaUpdate(SQLModel):
    schema_type: Optional[SchemaTypes] = None
    version_tag: Optional[str] = None
    comment: Optional[str] = None
    schema_path: Optional[str] = None
    schema_dependencies_path: Optional[str] = None
    platform_version: Optional[str] = None


class SchemaReturn(SchemaBase):
    schema_type: Optional[SchemaTypes] = None
    commit_id: Optional[str] = None
    version_tag: Optional[str] = None
    comment: Optional[str] = None
    schema_path: Optional[str] = None
    schema_dependencies_path: Optional[str] = None
    platform_version: Optional[str] = None
