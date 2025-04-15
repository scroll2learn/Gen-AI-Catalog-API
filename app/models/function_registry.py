from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config


class FunctionRegistryBase(SQLModel):
    function_id: int = Field(default=None, primary_key=True)
    function_name: str = Field(..., description="Function Name")
    function_key: Optional[str] = Field(default=None, description="Function Key")
    function_desc: str = Field(..., description="Function Description")
    function_inputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Function Inputs")
    function_outputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Function Outputs")


class FunctionRegistry(FunctionRegistryBase, TimestampModel, table=True):
    __tablename__ = "function_registry"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class FunctionRegistryCreate(FunctionRegistryBase):
    pass


class FunctionRegistryUpdate(SQLModel):
    function_desc: str = Field(..., description="Function Description")
    function_inputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Function Inputs")
    function_outputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Function Outputs")


class FunctionRegistryReturn(FunctionRegistryBase):
    pass
