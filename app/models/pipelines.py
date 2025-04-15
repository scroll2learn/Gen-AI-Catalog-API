from typing import Optional, List, Dict
from app.enums.connection_registry import SourceType
from app.models.base import TimestampModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, JSON, Relationship
from datetime import datetime
from app.core.config import Config
from app.models.base import TimestampModel
from app.models.bh_project import BHProject, ProjectEnvironment
from app.enums.bh_project import Status
from sqlalchemy.types import JSON
from pgvector.sqlalchemy import Vector
from app.enums.pipeline import ParameterType
from sqlalchemy import UniqueConstraint
 
 
class PipelineBase(SQLModel):
    """
    Base model for Pipeline, contains the basic information of a pipeline
    """
    pipeline_id: int = Field(default=None, primary_key=True)
 
    pipeline_name: str = Field(
        ..., description="Represents the name of the pipeline, human readable"
    )
    pipeline_key: str = Field(
        nullable=True,
        description="Unique pipeline key, no spaces or special characters",
    )
    bh_project_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key=f"{Config.DB_SCHEMA}.bh_project.bh_project_id"
    )
    notes: Optional[str] = Field(default=None, nullable=True, description="Notes")
 
    tags: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Tags for lineage, user defined",
    )
 
    status: Status = Field(
        default=Status.ACTIVE, nullable=True, description="Status for pipeline"
    )
 
    pipeline_version_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key=f"{Config.DB_SCHEMA}.pipeline_version.pipeline_version_id"
    )
    pipeline_json: Optional[dict] = Field(
    default=None,
    sa_column=Column(JSON, nullable=True),
    description="Pipeline JSON definition, contains the actual pipeline configuration",
    )
    pipeline_name_embedding: Optional[List[float]] = Field(
        sa_column=Column(Vector(768), nullable=True),
        description="Embedding for data source name and description"
    )

class Pipeline(PipelineBase, TimestampModel, table=True):
    """
    Model for Pipeline, contains the basic information of a pipeline
 
    Represents a pipeline in the system, contains metadata about the pipeline
    """
 
    __tablename__ = "pipeline"
    __table_args__ = {'schema': Config.DB_SCHEMA}
 
    bh_project: Optional["BHProject"] = Relationship(
        back_populates="pipeline",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
 
    # Relationship to PipelineDefinition
    pipeline_definitions: Optional["PipelineDefinition"] = Relationship(
        back_populates="pipeline",
        sa_relationship_kwargs={"uselist": False, "lazy": "selectin"},
    )
 
    pipeline_config: Optional["PipelineConfig"] = Relationship(
        back_populates="pipeline",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    pipeline_parameters: Optional["PipelineParameter"] = Relationship(
        back_populates="pipeline",
        sa_relationship_kwargs={"uselist": True, "lazy": "selectin"},
    )
    created_by_user: Optional["UserDetail"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Pipeline.created_by == UserDetail.user_detail_id",
            "lazy": "selectin",
        }
    )

    # Relationship with UserDetail for updated_by
    updated_by_user: Optional["UserDetail"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Pipeline.updated_by == UserDetail.user_detail_id",
            "lazy": "selectin",
        }
    )

 
class PipelineUpdate(SQLModel):
    pipeline_name: Optional[str] = None    
    pipeline_key: Optional[str] = None
    tags: Optional[dict] = None
    notes: Optional[str] = None
    pipeline_version_id: Optional[int] = None
    updated_by: Optional[int] = None
    pipeline_json: Optional[dict] = None
 
class PipelineCreate(SQLModel):
    pipeline_name: str
    bh_project_id: Optional[int]
    notes: Optional[str] = None
    tags: Optional[dict] = None
    pipeline_json: Optional[dict] = None
    
 
class PipelineDefinitionBase(SQLModel):
    """
    Model for PipelineDefinition, contains the pipeline definition
 
    Represents a pipeline definition in the system, contains the pipeline json definition
    """
 
    pipeline_definition_id: int = Field(
        default=None,
        primary_key=True,
        description="Primary key for pipeline definition",
    )
 
    pipeline_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.pipeline.pipeline_id",
        description="Foregin key to the pipeline table"
    )
 
    pipeline_json: Optional[dict] = Field(
        nullable=True,
        default=None,
        sa_column=Column(JSON),
        description="Pipeline JSON definition, contains the actual pipeline configuration",
    )
    schema_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.schema.schema_id",
    )
 
 
class PipelineDefinition(PipelineDefinitionBase, TimestampModel, table=True):
    """
    Model for PipelineDefinition, contains the pipeline definition
 
    Represents a pipeline definition in the system, contains the pipeline json definition
    """
 
    __tablename__ = "pipeline_definitions"
    __table_args__ = {'schema': Config.DB_SCHEMA}
 
    pipeline: Pipeline = Relationship(back_populates="pipeline_definitions")
 
 
class PipelineDefinitionCreate(SQLModel):
    pipeline_id: int
    pipeline_json: Optional[dict]
 
 
class PipelineDefinitionUpdate(SQLModel):
    pipeline_id: Optional[int] = None
    pipeline_json: Optional[dict] = {}
 
 
class PipelineReturn(SQLModel):
    pipeline_id: Optional[int]
    pipeline_name: Optional[str]
    pipeline_key: Optional[str]
    notes: Optional[str]
    tags: Optional[dict]
    bh_project_name: Optional[str] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    pipeline_json: Optional[dict] = None
    created_by_username: Optional[str] = None
    updated_by_username: Optional[str] = None
 
 
class PipelineDefinitionReturn(PipelineDefinitionBase, TimestampModel):
    pass
 
 
class PipelineVersionBase(SQLModel):
    pipeline_version_id: int = Field(
        default=None, primary_key=True, description="Primary key for the pipeline version"
    )
    commit_id: str = Field(
        ..., description="GitHub commit ID associated with the pipeline version"
    )
    version_tag: str = Field(..., description="GitHub tag for the pipeline version")
    comment: str = Field(
        ..., description="GitHub comment associated with the pipeline version"
    )
 
class PipelineVersion(PipelineVersionBase, TimestampModel, table=True):
    __tablename__ = "pipeline_version"
    __table_args__ = {"schema": Config.DB_SCHEMA}
 
 
class PipelineVersionCreate(SQLModel):
    pipeline_id: int
    comment: str
 
class PipelineVersionUpdate(SQLModel):
    version_tag: str = None
    comment: str = None
 
class PipelineVersionReturn(PipelineVersionBase, TimestampModel):
    pass
 
 
class PipelineConfigBase(SQLModel):
    pipeline_config_id: int = Field(
        default=None, primary_key=True, description="Primary key for the pipeline config"
    )
    pipeline_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.pipeline.pipeline_id",
        description="Foreign key to the pipeline table",
    )
    pipeline_config: dict = Field(
        sa_column=Column(JSON), description="pipeline configuration stored as JSON"
    )
 
class PipelineConfig(PipelineConfigBase, TimestampModel, table=True):
    __tablename__ = "pipeline_config"
    __table_args__ = {"schema": Config.DB_SCHEMA}
 
    # relationship with flow
    pipeline: Pipeline = Relationship(back_populates="pipeline_config")
 
class PipelineConfigCreate(SQLModel):
    pipeline_id: int
    pipeline_config: dict = {}
 
class PipelineConfigUpdate(SQLModel):
    pipeline_config: Optional[dict] = {}
 
class PipelineConfigReturn(PipelineConfig, TimestampModel):
    pass
 
class PipelineValidationError(SQLModel, table=True):
    """
    Model for Pipeline Validation Errors, contains error information for a pipeline
 
    Represents a validation error for a pipeline in the system, contains the error message and associated pipeline ID
    """
 
    __tablename__ = "pipeline_validation_errors"
    __table_args__ = {'schema': Config.DB_SCHEMA}
 
    error_id: int = Field(default=None, primary_key=True)
    pipeline_id: int = Field(
        ..., foreign_key=f"{Config.DB_SCHEMA}.pipeline.pipeline_id", description="Associated Pipeline ID"
    )
    transformation_name: str = Field(
        ..., description="Name of the transformation causing the error"
    )
    error_message: str = Field(..., description="Error message for the validation")
 
class PipelineValidationErrorUpdate(SQLModel):
    transformation_name: Optional[str] = None
    error_message: Optional[str] = None
 
 
class PipelineValidationErrorReturn(PipelineValidationError):
    pass


class PipelineConnectionBase(SQLModel):
    pipeline_connection_id : int = Field(default=None, primary_key=True)
    logical_name : str = Field(..., description="The logical name of the connection")
    connection_type : SourceType = Field(..., description="The type of the connection")
    tags: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Tags for lineage, user defined",
    )
    bh_env_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id",
    )
    client_project_id: str = Field(
        ...,
        description="The client project id of the connection"
    )
    client_secret_manager_key : str = Field(
        ...,
        description="The client secret manager key of the connection"
    )
    

class PipelineConnection(PipelineConnectionBase, TimestampModel, table=True):
    __tablename__ = "pipeline_connection"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    project_environment: ProjectEnvironment = Relationship(
        back_populates="pipeline_connection"
    )

class PipelineConnectionCreate(SQLModel):
    logical_name: str
    connection_type: SourceType
    tags: Optional[dict]
    bh_env_id: int
    client_project_id: str
    client_secret_manager_key: str


class PipelineConnectionUpdate(SQLModel):
    logical_name: Optional[str]
    connection_type: Optional[SourceType]
    tags: Optional[dict]
    bh_env_id: Optional[int]
    client_project_id: Optional[str]
    client_secret_manager_key: Optional[str]


class PipelineConnectionReturn(PipelineConnectionBase, TimestampModel):
    pass


class PipelineParameterBase(SQLModel):
    pipeline_parameter_id: int = Field(default=None, primary_key=True)
    pipeline_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.pipeline.pipeline_id",
        description="Foreign key to the pipeline table",
    )
    parameter_name: str = Field(..., description="The name of the parameter")
    parameter_value: str = Field(..., description="The value of the parameter")
    parameter_type: ParameterType = Field(..., description="The type of the parameter")


class PipelineParameter(PipelineParameterBase, TimestampModel, table=True):
    __tablename__ = "pipeline_parameter"
    __table_args__ = (
        UniqueConstraint('pipeline_id', 'parameter_name', 'parameter_type', name='uq_pipeline_parameter'),
        {"schema": Config.DB_SCHEMA}
    )

    pipeline: Pipeline = Relationship(back_populates="pipeline_parameters")


class PipelineParameterCreate(SQLModel):
    pipeline_id: int
    parameter_name: str
    parameter_value: str
    parameter_type: ParameterType


class PipelineParameterUpdate(SQLModel):
    pipeline_id: Optional[int]
    parameter_name: Optional[str]
    parameter_value: Optional[str]
    parameter_type: Optional[ParameterType]


class PipelineParameterReturn(PipelineParameterBase, TimestampModel):
    pass
