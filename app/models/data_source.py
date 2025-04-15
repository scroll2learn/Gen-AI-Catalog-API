from typing import Optional, List
from app.enums.bh_project import Status
from app.models.data_source_layout import DataSourceLayoutReturn
from sqlalchemy import Column, DateTime, text
from sqlmodel import SQLModel, Field, JSON, Relationship
from datetime import datetime
 
from app.models.bh_project import BHProject
from app.models.connection_registry import ConnectionConfig
from app.models.base import TimestampModel
from app.models import LakeZone
from app.core.config import Config
from pgvector.sqlalchemy import Vector
 
'''
DataSource -> Will have one entry for each data source
Layout -> Each datasource could have 'n' number of layout. This is especially done to support sources with multiple layouts.
Fields -> Each layout will have multiple fields
Validation -> Each field will have 'n' number of validations
TransformationRule -> In case of a derived field, this table will hold rules for deriving the field.
'''
 
# Base model for DataSource
class DataSourceBase(SQLModel):
    data_src_id: int = Field(default=None, primary_key=True)
    data_src_name: str = Field(..., min_length=1, description="The name of the cloud project")
    data_src_desc: str = Field(default=None, nullable=True, description="Description of the project")
    data_src_tags: dict = Field(default=None, sa_column=Column(JSON, nullable=True), description="Tags for lineage")
    data_src_last_updated: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
        )
    )
    data_src_quality: str = Field(default='0%', nullable=True, description="Quality of the datasource in percentage")
    data_src_status_cd: int = Field(default=None, nullable=True, description="Status of datasource (Active, Inactive, or Draft)")
    data_src_status: Optional[Status] = Field(default=Status.ACTIVE, nullable=True, description="Status of the project")
    # Foreign Keys
    lake_zone_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.lake_zone.lake_zone_id")
    connection_config_id: int = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.bh_connection_config.id")
    bh_project_id: int = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.bh_project.bh_project_id")
    owner: int = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.bh_user.bh_user_id")
 
    # Platform Managed Attributes
    data_src_key: str = Field(default=None, nullable=True, description="The key of the datasource")
 
    # New Fields
    file_name: str = Field(default=None, nullable=True, description="The name of the file associated with the datasource")
    file_path_prefix: str = Field(default=None, nullable=True, description="The path prefix where the file is stored")
    data_src_embeddings: Optional[List[float]] = Field(
        sa_column=Column(Vector(1536), nullable=True),
        description="Embedding for data source name and description"
    )
    data_src_relationships: str = Field(default=None, nullable=True, description="The relationships of the datasource")
    data_src_relationships_embeddings: Optional[List[float]] = Field(
        sa_column=Column(Vector(768), nullable=True),
        description="Embedding for data source relationships"
    )
 
 
# Full model for DataSource
class DataSource(DataSourceBase, TimestampModel, table=True):
    __tablename__ = "data_source"
    __table_args__ = {'schema': Config.DB_SCHEMA}
 
    # Relationships with Parent
    lake_zone: Optional[LakeZone] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    connection_config: Optional[ConnectionConfig] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    bh_project: Optional[BHProject] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    
    # Relationships with children
    data_source_metadata: Optional[List["DataSourceMetadata"]] = Relationship(
        back_populates="data_source", sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    data_source_layout: Optional[List["DataSourceLayout"]] = Relationship(
        back_populates="data_source", sa_relationship_kwargs={"lazy": "selectin"}
    )
 
# DTO models for creating and updating DataSource
class DataSourceCreate(SQLModel):
    data_src_id: Optional[int] = None
    data_src_name: str
    data_src_desc: Optional[str] = None
    data_src_tags: Optional[dict] = None
    lake_zone_id: Optional[int] = None
    data_src_key: Optional[str] = None
    connection_config_id: Optional[int] = None
    bh_project_id: Optional[int] = None
    data_src_quality: Optional[str] = None
    data_src_status_cd: Optional[int] = None
    file_name: Optional[str] = None
    connection_type: Optional[str] = None
    file_path_prefix: Optional[str] = None
    data_src_relationships: Optional[str] = None
 
 
class DataSourceUpdate(SQLModel):
    data_src_name: Optional[str] = None
    data_src_desc: Optional[str] = None
    data_src_status_cd: Optional[int] = None
    data_src_tags: Optional[dict] = None
    connection_config_id: Optional[int] = None
    bh_project_id: Optional[int] = None
    owner: Optional[int] = None
    data_src_embeddings: Optional[List[float]] = None
    data_src_relationships: Optional[str] = None
 
 
# Base model for DataSourceMetadata
class DataSourceMetadataBase(SQLModel):
    data_src_mtd_id: int = Field(default=None, primary_key=True)
    data_src_mtd_name: str = Field(..., min_length=1, description="The name of the metadata")
    data_src_mtd_value: str = Field(..., min_length=1, description="The value of the metadata")
    data_src_mtd_datatype_cd: int = Field(..., description="The datatype of the metadata")
    data_src_mtd_type_cd: int = Field(..., description="The type of the metadata")
    data_src_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id")
 
    # Platform Managed Attributes
    data_src_mtd_key: str = Field(default=None, nullable=True, description="The key of the metadata")
 
 
# Full model for DataSourceMetadata
class DataSourceMetadata(DataSourceMetadataBase, TimestampModel, table=True):
    __tablename__ = "data_source_metadata"
    __table_args__ = {'schema': Config.DB_SCHEMA}
 
    # Relationships with Parent
    data_source: DataSource = Relationship(back_populates="data_source_metadata")
 
 
# DTO models for creating and updating DataSourceMetadata
class DataSourceMetadataCreate(DataSourceMetadataBase):
    pass
 
 
class DataSourceMetadataUpdate(SQLModel):
    data_src_mtd_value: str
    data_src_mtd_datatype_cd: int
    data_src_mtd_type_cd: int
 
 
class DataSourceMetadataReturn(DataSourceMetadataBase):
    pass
 
 
# Return model for DataSource with metadata and additional attributes
class DataSourceReturn(TimestampModel):
    data_src_id: Optional[int] = None
    data_src_name: Optional[str] = None
    data_src_desc: Optional[str] = None
    data_src_tags: Optional[dict] = None
    lake_zone_id: Optional[int] = None
    data_src_key: Optional[str] = None
    connection_config_id: Optional[int] = None
    bh_project_id: Optional[int] = None
    data_src_quality: Optional[str] = None
    data_src_status_cd: Optional[int] = None
    file_name: Optional[str] = None
    connection_type: Optional[str] = None
    file_path_prefix: Optional[str] = None
    data_source_metadata: Optional[List[DataSourceMetadataReturn]] = []
    bh_project_name: Optional[str] = None
    total_records: Optional[int] = 0
    total_customer: Optional[int] = 0
    data_source_layout: Optional[List[DataSourceLayoutReturn]] = None
    connection_config: Optional[ConnectionConfig] = None
    data_src_relationships: Optional[str] = None

DataSourceReturn.update_forward_refs()
