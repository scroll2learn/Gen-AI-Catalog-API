from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config
'''
DataSource -> Will have one entry for each data source
Layout -> Each datasource could have 'n' number of layout. this is espeecially done to support source with multiple layouts
Fields -> Eachn layout will have multiple fields
Validation -> Each field will have 'n' number of validation
TransformaonRule -> In case of a derived filed, this table will hold rules for deriving the field
'''

class LayoutFieldsDQBase(SQLModel):
    fld_dq_id: int = Field(default=None, primary_key=True)
    fld_dq_params: dict = Field(default=None, sa_column=Column(JSON, nullable=True), description="Data Quality Parameters")
    fld_dq_level: str = Field(..., description="Data Quality Level")

    # Foreign Keys
    lyt_fld_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.layout_fields.lyt_fld_id", description="Field ID")
    fld_dq_type_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.fld_dq_types.dq_id", description="Data Quality Type")


class LayoutFieldsDQ(LayoutFieldsDQBase, TimestampModel, table=True):
    __tablename__ = "layout_fields_dq"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class LayoutFieldsDQCreate(LayoutFieldsDQBase): 
    pass


class LayoutFieldsDQUpdate(SQLModel):
    fld_dq_params: dict
    fld_dq_level: str = None


class LayoutFieldsDQReturn(LayoutFieldsDQBase, TimestampModel):
    pass
