from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.models.base import TimestampModel
from app.core.config import Config


'''
DataSource -> Will have one entry for each data source
Layout -> Each datasource could have 'n' number of layout. this is espeecially done to support source with multiple layouts
Fields -> Eachn layout will have multiple fields
Validation -> Each field will have 'n' number of validation
TransformaonRule -> In case of a derived filed, this table will hold rules for deriving the field
'''

class DataSourceLayoutBase(SQLModel):
    data_src_lyt_id: int = Field(default=None, primary_key=True)
    data_src_lyt_name: str = Field(..., min_length=1, description="The name of the layout")
    data_src_lyt_fmt_cd: int = Field(default=None, nullable=False, description="Foreign key to data source layout format code")
    data_src_lyt_delimiter_cd: Optional[int] = Field(default=None, nullable=True, description="Foreign key to data source layout delimiter code")
    data_src_lyt_cust_delimiter: Optional[str] = Field(default=None, nullable=True, description="Custom delimiter")
    data_src_lyt_header: Optional[bool] = Field(default=False, nullable=True, description="Header row")
    data_src_lyt_encoding: Optional[str] = Field(default=None, nullable=True, description="Foreign key to data source layout encoding code")
    data_src_lyt_quote_chars_cd: Optional[int] = Field(default=None, nullable=True, description="Foreign key to data source layout quote chars code")
    data_src_lyt_escape_chars_cd: Optional[int] = Field(default=None, nullable=True, description="Foreign key to data source layout escape chars code")
    data_src_lyt_regex: Optional[str] = Field(default=None, nullable=True, description="Regex to validate the layout")
    data_src_lyt_pk: bool = Field(default=True, nullable=False, description="Primary Key")
    data_src_lyt_total_records: Optional[int] = Field(default=None, nullable=True, description="Total records in the layout")
    data_src_lyt_type_cd: int = Field(default=None, nullable=False, description="source layout type code like Master, Child")
    data_src_lyt_is_mandatory: bool = Field(default=True, nullable=False, description="True & False")
    data_src_n_rows_to_skip: Optional[int] = Field(default=0, nullable=True, description="Number of rows to skip")
    data_src_file_path: Optional[str] = Field(default=None, nullable=True, description="File path for Onboarding")
    data_src_file_type: Optional[str] = Field(default=None, nullable=True, description="File type as full or incremental")
    data_src_multi_part_file: Optional[bool] = Field(default=False, nullable=True, description="Multi part file or not")
    data_src_is_history_required: Optional[bool] = Field(default=False, nullable=True, description="History required or not")

    # Foreign Keys
    data_src_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id")

    # Platform Managed Attributes
    data_src_lyt_key: str = Field(default=None, nullable=True, description="The key of the layout")


class DataSourceLayout(DataSourceLayoutBase, TimestampModel, table=True):
    __tablename__ = "data_source_layout"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    data_source: "DataSource" = Relationship(back_populates="data_source_layout")

    # Relationships with children
    layout_fields: Optional[List["LayoutFields"]] = Relationship(back_populates="data_source_layout", sa_relationship_kwargs={"lazy": "selectin"})


class DataSourceLayoutCreate(DataSourceLayoutBase): 
    pass


class DataSourceLayoutUpdate(SQLModel):
    data_src_lyt_fmt_cd: int = None
    data_src_lyt_delimiter_cd: Optional[int] = None
    data_src_lyt_cust_delimiter: Optional[str] = None
    data_src_lyt_header: Optional[bool] = False
    data_src_lyt_encoding_cd: Optional[int] = None
    data_src_lyt_quote_chars_cd: Optional[int] = None
    data_src_lyt_escape_chars_cd: Optional[int] = None
    data_src_lyt_regex: Optional[str] = None
    data_src_lyt_pk: Optional[bool] = False
    data_src_file_type: Optional[str] = None
    data_src_is_history_required: Optional[bool] = False


class DataSourceLayoutReturn(SQLModel):
    data_src_lyt_id: Optional[int] = None
    data_src_lyt_name: Optional[str] = None
    data_src_lyt_fmt_cd: Optional[int] = None
    data_src_lyt_delimiter_cd: Optional[int] = None
    data_src_lyt_cust_delimiter: Optional[str] = None
    data_src_lyt_header: Optional[bool] = None
    data_src_lyt_encoding_cd: Optional[int] = None
    data_src_lyt_quote_chars_cd: Optional[int] = None
    data_src_lyt_escape_chars_cd: Optional[int] = None
    data_src_lyt_regex: Optional[str] = None
    data_src_lyt_pk: Optional[bool] = None
    data_src_lyt_total_records: Optional[int] = None
    data_src_lyt_type_cd: Optional[int] = None
    data_src_lyt_is_mandatory: Optional[bool] = None
    data_src_id: Optional[int] = None


class DataSourceLayoutFullReturn(DataSourceLayoutBase, TimestampModel):
    from app.models.layout_fields import LayoutFieldsReturn
    from app.models.connection_registry import ConnectionConfigReturn
    
    layout_fields: Optional[List[LayoutFieldsReturn]] = []
    connection_config: Optional[ConnectionConfigReturn] = None
