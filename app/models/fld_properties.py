from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config


class FieldPropertiesBase(SQLModel):
    fld_id: int = Field(default=None, primary_key=True)
    fld_name: str = Field(..., min_length=1, max_length=64, description="The name of the Field")
    fld_key: str = Field(..., min_length=1, max_length=64, description="The key of the Field")
    fld_datatype: str = Field(..., min_length=1, max_length=64, description="The datatype of the Field")
    is_fld_unique: bool = Field(default=False, nullable=False, description="Is the field unique")
    is_fld_mandatory: bool = Field(default=False, nullable=False, description="Is the field mandatory")
    is_fld_categorical: bool = Field(default=False, nullable=False, description="Is the field categorical")
    is_fld_date: bool = Field(default=False, nullable=False, description="Is the field date type")
    is_fld_boolean: bool = Field(default=False, nullable=False, description="Is the field boolean")
    is_fld_numeric: bool = Field(default=False, nullable=False, description="Is the field numeric")
    is_fld_text: bool = Field(default=False, nullable=False, description="Is the field text")
    fld_min_value: Optional[str] = Field(default=None, nullable=True, description="Minimum value of the field")
    fld_max_value: Optional[str] = Field(default=None, nullable=True, description="Maximum value of the field")
    fld_valid_values: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Valid values for the field")
    fld_top_counts: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Top counts for the field")
    lyt_id: Optional[int] = Field(default=None, nullable=True, description="The layout id")

class FieldProperties(FieldPropertiesBase, TimestampModel, table=True):
    __tablename__ = "fld_properties"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class FieldPropertiesCreate(FieldProperties):
    pass


class FieldPropertiesUpdate(SQLModel):
    fld_datatype: str = Field(..., min_length=1, max_length=64, description="The datatype of the Field")
    is_fld_unique: bool = Field(default=False, nullable=False, description="Is the field unique")
    is_fld_mandatory: bool = Field(default=False, nullable=False, description="Is the field mandatory")
    is_fld_categorical: bool = Field(default=False, nullable=False, description="Is the field categorical")
    is_fld_date: bool = Field(default=False, nullable=False, description="Is the field date type")
    is_fld_boolean: bool = Field(default=False, nullable=False, description="Is the field boolean")
    is_fld_numeric: bool = Field(default=False, nullable=False, description="Is the field numeric")
    is_fld_text: bool = Field(default=False, nullable=False, description="Is the field text")
    fld_min_value: Optional[str] = Field(default=None, nullable=True, description="Minimum value of the field")
    fld_max_value: Optional[str] = Field(default=None, nullable=True, description="Maximum value of the field")
    fld_valid_values: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Valid values for the field")
    fld_top_counts: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Top counts for the field")


class FieldPropertiesReturn(FieldPropertiesBase, TimestampModel):
    pass
