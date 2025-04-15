from typing import Optional, List
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship

from app.models.base import TimestampModel
from app.core.config import Config
from pgvector.sqlalchemy import Vector

'''
DataSource -> Will have one entry for each data source
Layout -> Each datasource could have 'n' number of layout. this is espeecially done to support source with multiple layouts
Fields -> Eachn layout will have multiple fields
Validation -> Each field will have 'n' number of validation
TransformaonRule -> In case of a derived filed, this table will hold rules for deriving the field
'''

class LayoutFieldsBase(SQLModel):
    lyt_fld_id: int = Field(default=None, primary_key=True)
    lyt_fld_name: str = Field(..., min_length=1, max_length=64, description="The name of the Field")
    lyt_fld_desc: Optional[str] = Field(default=None, max_length=255, description="The description of the Field")
    lyt_fld_order: int = Field(..., nullable=False, description="Order of the field")
    lyt_fld_is_pk: bool = Field(default=False, nullable=False, description="Primary Key")
    lyt_fld_start: Optional[int] = Field(default=None, nullable=True, description="Start position of the field")
    lyt_fld_length: Optional[int] = Field(default=None, nullable=True, description="Length of the field")
    lyt_fld_data_type_cd: int = Field(..., description="Data type cd of the field")
    lyt_fld_tags: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Tags for lineage")
    lyt_fld_data_type: Optional[str] = Field(default=None, nullable=True, description="Data type of the field")
    lyt_fld_source_data_type: Optional[str] = Field(default=None, nullable=True, description="Source Data type of the field")
    # Foreign Keys
    lyt_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.data_source_layout.data_src_lyt_id")

    # Platform Managed Attributes
    lyt_fld_key: str = Field(..., min_length=1, max_length=64, description="The key of the Field")

    lyt_fld_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(1536), nullable=True),
        description="Embedding for layout field name and description"
    )

class LayoutFields(LayoutFieldsBase, TimestampModel, table=True):
    __tablename__ = "layout_fields"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    from app.models.data_source_layout import DataSourceLayout
    data_source_layout: DataSourceLayout = Relationship(back_populates="layout_fields")


class LayoutFieldsCreate(SQLModel): 
    lyt_fld_id: int = None
    lyt_fld_name: str = None
    lyt_fld_desc: Optional[str] = None
    lyt_fld_order: int = None
    lyt_fld_is_pk: bool = None
    lyt_fld_start: Optional[int] = None
    lyt_fld_length: Optional[int] = None
    lyt_fld_data_type_cd: int = None
    lyt_fld_tags: Optional[dict] = None
    lyt_id: int = None
    lyt_fld_key: str = None
    lyt_fld_data_type: Optional[str] = None


class LayoutFieldsUpdate(SQLModel):
    lyt_fld_name: Optional[str] = None
    lyt_fld_desc: Optional[str] = None
    lyt_fld_is_pk: Optional[bool] = None
    lyt_fld_start: Optional[int] = None
    lyt_fld_length: Optional[int] = None
    lyt_fld_data_type_cd: Optional[int] = None
    lyt_fld_tags: Optional[dict]  = None
    lyt_fld_data_type: Optional[str] = None
    lyt_fld_embedding: Optional[List[float]] = None
    
class LayoutDescriptionUpdate(SQLModel):
    lyt_fld_id: int
    lyt_fld_desc: Optional[str] = None

class LayoutBulkDescriptionUpdate(SQLModel):
    descriptions: List[LayoutDescriptionUpdate]


class LayoutFieldsReturn(LayoutFieldsCreate, TimestampModel):
    pass

