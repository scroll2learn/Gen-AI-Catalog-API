from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config


class FieldDQTypesBase(SQLModel):
    dq_id: Optional[int] = Field(default=None, primary_key=True)
    dq_name: str = Field(..., description="Validation Name")
    dq_template: str = Field(default=None, description="Validation Template")
    dq_lookup: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Validation Lookup")
    dq_inputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Validation Inputs")


class FieldDQTypes(FieldDQTypesBase, TimestampModel, table=True):
    __tablename__ = "fld_dq_types"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class FieldDQTypesCreate(FieldDQTypesBase):
    pass


class FieldDQTypesUpdate(SQLModel):
    dq_name: str
    dq_template: str
    dq_lookup: Optional[dict] = None
    dq_inputs: Optional[dict] = None


class FieldDQReturn(FieldDQTypesBase, TimestampModel):
    pass
