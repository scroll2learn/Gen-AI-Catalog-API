from typing import Optional, List, Dict
from app.enums.bh_project import Status
from app.models.bh_project import BHProject, ProjectEnvironment
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship

from app.models.base import TimestampModel
from app.core.config import Config
from pydantic import EmailStr
from datetime import datetime


class FlowBase(SQLModel):
    flow_id: int = Field(default=None, primary_key=True)
    flow_name: str = Field(..., description="Represents the name of the flow")
    flow_key: str = Field(
        default=None,
        nullable=True,
        description="Represents the unique key of the flow ,should allow small letters with underscore only",
    )
    bh_project_id: int = Field(
        default=None,
        nullable=False,
        foreign_key=f"{Config.DB_SCHEMA}.bh_project.bh_project_id",
    )
    recipient_email: Optional[dict] = Field( 
        
        sa_column=Column(JSON, nullable=True), 
        description="Recipients' emails"
    )
    notes: Optional[str] = Field(default=None, nullable=True, description="Notes")
    tags: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Tags for lineage",
    )
    status: Status = Field(
        default=Status.ACTIVE, nullable=True, description="Status of the flow"
    )
    alert_settings: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=True),
        description="Alert settings for job events",
    )

    bh_bundle_id: Optional[int] = Field(default=None,nullable=True, foreign_key=f"{Config.DB_SCHEMA}.bh_bundle.bh_bundle_id")


class Flow(FlowBase, TimestampModel, table=True):
    __tablename__ = "flow"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # relationship with Flowdeployment
    flow_deployment: Optional[List["FlowDeployment"]] = Relationship(
        back_populates="flow", sa_relationship_kwargs={"lazy": "selectin"}
    )

    flow_definition: Optional["FlowDefinition"] = Relationship(
        back_populates="flow",
        sa_relationship_kwargs={"uselist": False, "lazy": "selectin"},
    )

    # relationship with Project
    bh_project: Optional["BHProject"] = Relationship(
        back_populates="flow", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # relationship with flow config
    flow_config: Optional["FlowConfig"] = Relationship(
        back_populates="flow", sa_relationship_kwargs={"lazy": "selectin"}
    )

    bh_bundle:Optional["BHReleaseBundle"] = Relationship(
        back_populates="flow", sa_relationship_kwargs={"lazy": "selectin"}
    )
    flow_version: Optional["FlowVersion"] = Relationship(
        back_populates="flow", sa_relationship_kwargs={"lazy": "selectin"}
    )
    # Relationship with UserDetail for created_by
    created_by_user: Optional["UserDetail"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Flow.created_by == UserDetail.user_detail_id",
            "lazy": "selectin",
        }
    )

    # Relationship with UserDetail for updated_by
    updated_by_user: Optional["UserDetail"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Flow.updated_by == UserDetail.user_detail_id",
            "lazy": "selectin",
        }
    )

class FlowUpdate(SQLModel):
    flow_name: Optional[str] = None
    flow_key: Optional[str] = None
    recipient_email: Optional[dict] = None
    notes: Optional[str] = None
    tags: Optional[dict] = None
    updated_by: Optional[int] = None


class FlowCreate(SQLModel):
    flow_name: str
    recipient_email: Optional[dict] 
    notes: Optional[str] = None
    tags: Optional[dict] = None
    bh_project_id: Optional[int] = None
    alert_settings: Optional[dict] = {
        "on_job_start": False,
        "on_job_failure": False,
        "on_job_success": False,
        "long_running": False,
    }
    flow_json: Optional[dict]
    bh_env_id: Optional[int]


class FlowDeploymentBase(SQLModel):
    flow_deployment_id: int = Field(default=None, primary_key=True)
    flow_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.flow.flow_id")
    bh_env_id: int = Field(
        default=None,
        nullable=False,
        foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id",
    )
    flow_version_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key=f"{Config.DB_SCHEMA}.flow_version.flow_version_id",
    )
    schema_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key=f"{Config.DB_SCHEMA}.schema.schema_id",
        description="Foreign key to the schema table",
    )
    cron_expression: Optional[dict] = Field(
        default=None,
        nullable=True,
        sa_column=Column(JSON, nullable=True),
        description="Flow Cron Expression",
    )


class FlowDeployment(FlowDeploymentBase, TimestampModel, table=True):
    __tablename__ = "flow_deployment"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # Relationship with Flow
    flow: Flow = Relationship(back_populates="flow_deployment")

    # Relationship with ProjectEnvironment
    project_environment: ProjectEnvironment = Relationship(
        back_populates="flow_deployment"
    )


class FlowDeploymentCreate(SQLModel):
    flow_id: Optional[int]
    bh_env_id: Optional[int]
    cron_expression: Optional[dict]


class FlowDeploymentUpdate(SQLModel):
    flow_id: Optional[int] = None
    bh_env_id: Optional[int] = None
    flow_version_id: Optional[int] = None
    schema_id: Optional[int] = None
    cron_expression: Optional[dict]


class FlowDeploymentReturn(FlowDeploymentBase):
    flow_name: Optional[str]
    bh_env_name: Optional[str]


class FlowDeploymentInFlowReturn(SQLModel):
    flow_deployment_id: Optional[int]
    bh_env_id: Optional[str]



class FlowCommit(SQLModel):
    flow_id: int = None
    commit_message: Optional[str] = None


class FlowDefinitionBase(SQLModel):
    flow_definition_id: int = Field(
        default=None,
        primary_key=True,
        description="Primary key for the flow definition",
    )
    flow_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.flow.flow_id",
        description="Foreign key to the flow table",
    )
    flow_json: Optional[dict] = Field(
        nullable=True,
        default=None,
        sa_column=Column(JSON),
        description="Flow JSON configuration",
    )
    schema_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.schema.schema_id",
        description="Foreign key to the schema table",
    )


class FlowDefinition(FlowDefinitionBase, TimestampModel, table=True):
    __tablename__ = "flow_definition"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # Relationship with Flow
    flow: Flow = Relationship(back_populates="flow_definition")


class FlowDefinitionCreate(SQLModel):
    flow_id: int
    flow_json: Optional[dict]


class FlowDefinitionUpdate(SQLModel):
    flow_id: Optional[int] = None
    flow_json: Optional[dict] = {}
    flow_deployment_id: int = None


class FlowDefinitionReturn(TimestampModel):
    flow_definition_id: Optional[int]
    flow_id: Optional[int]
    flow_json: Optional[dict]


class FlowVersionBase(SQLModel):
    flow_version_id: int = Field(
        default=None, primary_key=True, description="Primary key for the flow version"
    )
    commit_id: str = Field(
        ..., description="GitHub commit ID associated with the flow version"
    )
    version_tag: str = Field(..., description="GitHub tag for the flow version")
    comment: str = Field(
        ..., description="GitHub comment associated with the flow version"
    )
    flow_id: int = Field(
        nullable=True,
        default=None,
        foreign_key=f"{Config.DB_SCHEMA}.flow.flow_id",
        description="Foreign key to the flow table",
    )


class FlowVersion(FlowVersionBase, TimestampModel, table=True):
    __tablename__ = "flow_version"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    flow: Flow = Relationship(back_populates="flow_version")


class FlowVersionCreate(SQLModel):
    flow_deployment_id: int
    comment: str


class FlowVersionUpdate(SQLModel):
    version_tag: str = None
    comment: str = None


class FlowVersionReturn(FlowVersionBase, TimestampModel):
    pass


class FlowConfigBase(SQLModel):
    flow_config_id: int = Field(
        default=None, primary_key=True, description="Primary key for the flow config"
    )
    flow_id: int = Field(
        ...,
        foreign_key=f"{Config.DB_SCHEMA}.flow.flow_id",
        description="Foreign key to the flow table",
    )
    flow_config: dict = Field(
        sa_column=Column(JSON), description="Flow configuration stored as JSON"
    )


class FlowConfig(FlowConfigBase, TimestampModel, table=True):
    __tablename__ = "flow_config"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # relationship with flow
    flow: Flow = Relationship(back_populates="flow_config")


class FlowConfigCreate(SQLModel):
    flow_id: int
    flow_config: dict = {}


class FlowConfigUpdate(SQLModel):
    flow_config: Optional[dict] = {}


class FlowConfigReturn(TimestampModel):
    flow_config_id: Optional[int]
    flow_id: Optional[int]
    flow_config: Optional[dict]

class FlowReturn(SQLModel):
    flow_id: Optional[int]
    flow_name: Optional[str]
    flow_key: Optional[str]
    recipient_email: Optional[dict]
    notes: Optional[str]
    tags: Optional[dict]
    flow_deployment: Optional[List[FlowDeploymentReturn]] = []
    bh_project_name: Optional[str] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    flow_config: Optional[List[FlowConfigReturn]] = []
    flow_definition: Optional[FlowDefinitionReturn] = None
    created_by_username: Optional[str] = None
    updated_by_username: Optional[str] = None
