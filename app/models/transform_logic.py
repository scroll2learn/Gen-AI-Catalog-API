from typing import Optional, List
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship

from app.models.base import TimestampModel
from app.core.config import Config


class TransformLogicBase(SQLModel):
    transform_id: int = Field(default=None, primary_key=True)
    transform_desc: str = Field(..., description="Transformation Description")
    transform_inputs: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Parameters")
    transform_order: int = Field(..., description="Order of the transformation")

    # Foreign Keys
    transform_function_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.function_registry.function_id", description="Function ID")
    join_id: Optional[int] = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.joins.join_id", description="Join ID")
    pipeline_id: Optional[int] = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.pipeline.pipeline_id", description="Pipeline ID")


class TransformLogic(TransformLogicBase, TimestampModel, table=True):
    __tablename__ = "transform_logic"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with children
    transform_input_fields: Optional[List["TransformInputFields"]] = Relationship(back_populates="transform_logic", sa_relationship_kwargs={"lazy": "selectin"})
    transform_output_fields: Optional[List["TransformOutputFields"]] = Relationship(back_populates="transform_logic", sa_relationship_kwargs={"lazy": "selectin"})


class TransformLogicCreate(TransformLogicBase):
    pass


class TransformLogicUpdate(SQLModel):
    transform_desc: Optional[str] = None
    transform_inputs: Optional[dict] = None
    transform_order: Optional[int] = None
    join_id: Optional[int] = None
    pipeline_id: Optional[int] = None


class TransformInputFieldsBase(SQLModel):
    transform_input_field_id: int = Field(default=None, primary_key=True)

    # Foreign Keys
    lyt_fld_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.layout_fields.lyt_fld_id", description="Layout Field ID")
    transform_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.transform_logic.transform_id", description="Transformation ID")
    data_src_lyt_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source_layout.data_src_lyt_id", description="Data Source Layout ID")
    data_src_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id", description="Data Source ID")


class TransformInputFields(TransformInputFieldsBase, TimestampModel, table=True):
    __tablename__ = "transform_in_flds"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    transform_logic: TransformLogic = Relationship(back_populates="transform_input_fields")


class TransformInputFieldsCreate(TransformInputFieldsBase):
    pass


class TransformInputFieldsUpdate(SQLModel):
    lyt_fld_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.layout_fields.lyt_fld_id", description="Layout Field ID")
    data_src_lyt_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source_layout.data_src_lyt_id", description="Data Source Layout ID")
    data_src_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id", description="Data Source ID")


class TransformInputFieldsReturn(TransformInputFieldsBase, TimestampModel):
    pass


class TransformOutputFieldsBase(SQLModel):
    transform_output_field_id: int = Field(default=None, primary_key=True)
    output_field_name: str = Field(..., description="Output Field Name")

    # Platform Managed Attributes
    output_field_key: Optional[str] = Field(..., description="Output Field Key")

    # Foreign Keys
    transform_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.transform_logic.transform_id", description="Transformation ID")


class TransformOutputFields(TransformOutputFieldsBase, TimestampModel, table=True):
    __tablename__ = "transform_out_flds"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    transform_logic: TransformLogic = Relationship(back_populates="transform_output_fields")


class TransformOutputFieldsCreate(TransformOutputFieldsBase):
    pass


class TransformOutputFieldsUpdate(SQLModel):
    output_field_name: str = Field(..., description="Output Field Name")
    output_field_key: Optional[str] = Field(..., description="Output Field Key")


class TransformOutputFieldsReturn(TransformOutputFieldsBase, TimestampModel):
    pass


class TransformLogicReturn(TransformLogicBase, TimestampModel):
    transform_input_fields: Optional[List[TransformInputFieldsReturn]] = []
    transform_output_fields: Optional[List[TransformOutputFieldsReturn]] = []
