from typing import Optional, List
from app.enums.bh_project import Status
from app.enums.env import FlowConnectionType
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship
from pydantic import EmailStr, HttpUrl, AnyUrl

from app.models.base import TimestampModel
from app.core.config import Config
from app.models.pulish_data import PublishDetails


class BHProjectBase(SQLModel):
    bh_project_id: Optional[int] = Field(default=None, primary_key=True)
    bh_project_name: str = Field(..., min_length=1, description="The name of the project")
    bh_github_provider: Optional[int] = Field(default=None, nullable=True, foreign_key=f"{Config.DB_SCHEMA}.codes_dtl.id")
    bh_github_username: Optional[str] = Field(default=None, nullable=True, description="Github Username")
    bh_github_email: Optional[EmailStr] = Field(default=None, nullable=True, description="Email associated with the Github account")
    bh_default_branch: Optional[str] = Field(default='main', nullable=True, description="Default branch of the project")
    bh_github_url: Optional[HttpUrl] = Field(default=None, nullable=True, description="Github Repo URL")
    bh_github_token_url: Optional[str] = Field(default=None, nullable=True, description="Secret manager URL")
    status: Optional[Status] = Field(default=Status.ACTIVE, nullable=True, description="Status of the project")
    ytd_cost: Optional[float] = Field(default=0.00, nullable=True, description="Year to date cost")
    current_month_cost: Optional[float] = Field(default=0.00, nullable=True, description="Current month cost")
    total_storage: Optional[float] = Field(default=0.00, nullable=True, description="Total storage")
    tags: Optional[dict] = Field(default=None, nullable=True, sa_column=Column(JSON, nullable=True), description="Tags for lineage")
    repo_name: Optional[str] = Field(default=None, nullable=True, description="Github Repo Name")

class BHProject(BHProjectBase, TimestampModel, table=True):
    __tablename__ = "bh_project"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with children
    publish_details: List[PublishDetails] = Relationship(back_populates="bh_project", sa_relationship_kwargs={"lazy": "selectin"})
    data_source: List["DataSource"] = Relationship(back_populates="bh_project", sa_relationship_kwargs={"lazy": "selectin"})
    flow: List["Flow"] = Relationship(back_populates="bh_project", sa_relationship_kwargs={"lazy": "selectin"})
    pipeline: List["Pipeline"] = Relationship(back_populates="bh_project", sa_relationship_kwargs={"lazy": "selectin"})
    project_environment: List["ProjectEnvironment"] = Relationship(back_populates="bh_project", sa_relationship_kwargs={"lazy": "selectin"})

class BHProjectCreate(SQLModel):
    bh_project_name: str = None
    bh_github_provider: int = None
    bh_github_username: str = None
    bh_github_email: EmailStr = None
    bh_default_branch: str = None
    bh_github_url: HttpUrl = None
    bh_github_token_url: str = None
    tags: dict = None
    init_vector: str # Created freshly for every API Call


class BHProjectUpdate(SQLModel):
    bh_project_name: Optional[str] = None
    bh_github_provider: Optional[int] = None
    bh_github_username: Optional[str] = None
    bh_github_email: Optional[EmailStr] = None
    bh_default_branch: Optional[str] = None
    bh_github_url: Optional[HttpUrl] = None
    bh_github_token: Optional[str] = None
    status: Optional[Status] = None
    tags: Optional[dict] = None
    ytd_cost: Optional[float] = None
    current_month_cost: Optional[float] = None
    total_storage: Optional[float] = None 

class ProjectEnvironmentBase(SQLModel):
    # This Class represents project project_environment details.    
    bh_env_id: int = Field(default=None, primary_key=True)
    bh_env_name: str = Field(..., description="Name of the project_environment")
    bh_env_provider: int = Field(default=None, nullable=False, foreign_key=f"{Config.DB_SCHEMA}.codes_dtl.id")
    cloud_provider_cd: int = Field(default=None, nullable=False, foreign_key=f"{Config.DB_SCHEMA}.codes_dtl.id")
    cloud_region_cd: int = Field(..., description="Foreign key to cloud region code")   
    location: str = Field(default=None, nullable=True, description="Location of the project_environment")
    pvt_key: Optional[str] = Field(default=None, nullable=True, description="Private key url")
    status: Optional[Status] = Field(default=Status.ACTIVE, nullable=True, description="Status of the project_environment")
    tags: dict = Field(default=None, sa_column=Column(JSON, nullable=True), description="Tags for linege")
    project_id: Optional[str] = Field(default=None, nullable=True, description="project Id")
    airflow_url: Optional[str] = Field(default=None, nullable=True, description="airflow url")
    airflow_bucket_name: Optional[str] = Field(default=None, nullable=True, description="airflow bucket name")
    airflow_env_name: Optional[str] = Field(default=None, nullable=True, description="airflow env name")
    access_key: Optional[str] = Field(default=None, nullable=True, description="access key")
    bh_project_id: int = Field(
        default=None,
        nullable=True,
        foreign_key=f"{Config.DB_SCHEMA}.bh_project.bh_project_id",
    )

class ProjectEnvironment(ProjectEnvironmentBase, TimestampModel, table=True):
    __tablename__ = "project_environment"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with children
    lake_zone: Optional["LakeZone"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"uselist": False, "lazy": "selectin"})
    pre_configure_zone: Optional["PreConfigureZone"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"uselist": False, "lazy": "selectin"})
    configure_lifecycle: Optional["ConfigureLifecycle"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"uselist": False, "lazy": "selectin"})
    flow_connection: Optional["FlowConnection"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"uselist": False, "lazy": "selectin"})
    flow_deployment: Optional["FlowDeployment"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"lazy": "selectin"})
    bh_project: Optional["BHProject"] = Relationship(
        back_populates="project_environment", sa_relationship_kwargs={"lazy": "selectin"}
    )
    pipeline_connection: Optional["PipelineConnection"] = Relationship(back_populates="project_environment", sa_relationship_kwargs={"lazy": "selectin"})


class ProjectEnvironmentCreate(SQLModel): 
    bh_env_name: str = None
    bh_env_provider: int = None
    cloud_provider_cd: int = None
    cloud_region_cd: Optional[int] = None
    location: Optional[str] = None
    pvt_key: Optional[str] = None
    tags: Optional[dict] = None
    project_id: Optional[str] = None
    airflow_url: Optional[str] = None
    airflow_bucket_name: Optional[str] = None
    airflow_env_name: Optional[str] = None
    access_key: Optional[str] = None
    secret_access_key: Optional[str] = None

class ProjectEnvironmentUpdate(SQLModel):
    # Class for updating a new Project ProjectEnvironment. All fields are optional 
    bh_env_name: Optional[str] = None
    bh_env_provider: Optional[int] = None
    cloud_provider_cd: Optional[int] = None
    cloud_region_cd: Optional[int] = None
    location: Optional[str] = None
    pvt_key: Optional[str] = None
    status: Optional[Status] = None
    tags: Optional[dict] = None
    project_id: Optional[str] = None
    airflow_url: Optional[str] = None
    airflow_bucket_name: Optional[str] = None
    airflow_env_name: Optional[str] = None
    access_key: Optional[str] = None


class LakeZoneBase(SQLModel):
    lake_zone_id: int = Field(default=None, primary_key=True)
    lake_name: str = Field(default=None, nullable=True, description="Name of the lake zone")
    business_url: AnyUrl = Field(default=None, nullable=True, description="Business url of the lake zone")
    lake_description: str = Field(default=None, nullable=True, description="Description of the lake zone")

    # Foreign Keys
    bh_env_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id")


class LakeZone(LakeZoneBase, TimestampModel, table=True):
    __tablename__ = "lake_zone"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    project_environment: ProjectEnvironment = Relationship(back_populates="lake_zone")


class LakeZoneCreate(SQLModel):
    lake_name: str = None
    business_url: AnyUrl = None
    lake_description: str = None
    bh_env_id: int = None


class LakeZoneUpdate(SQLModel):
    lake_name: Optional[str] = None
    lake_description: Optional[str] = None
    business_url: Optional[AnyUrl] = None



class LakeZoneReturn(LakeZoneBase, TimestampModel):
    pass


class ProjectEnvironmentReturn(ProjectEnvironmentBase, TimestampModel):
    bh_env_provider_name: Optional[str] = None
    cloud_provider_name: Optional[str] = None
    secret_access_key: Optional[str] = None
    @classmethod
    def from_orm_with_aliases(cls, instance, bh_env_provider_alias, cloud_provider_alias):
        return cls(
            bh_env_id=instance.bh_env_id,
            bh_env_name=instance.bh_env_name,
            bh_env_provider=instance.bh_env_provider,
            cloud_provider_cd=instance.cloud_provider_cd,
            cloud_region_cd=instance.cloud_region_cd,
            location=instance.location,
            pvt_key=instance.pvt_key,
            status=instance.status,
            tags=instance.tags,
            project_id=instance.project_id,
            airflow_url=instance.airflow_url,
            airflow_bucket_name=instance.airflow_bucket_name,
            airflow_env_name=instance.airflow_env_name,
            access_key=instance.access_key,
            bh_env_provider_name=bh_env_provider_alias.dtl_desc if bh_env_provider_alias else None,
            cloud_provider_name=cloud_provider_alias.dtl_desc if cloud_provider_alias else None
        )
      
class BHProjectReturn(BHProjectBase, TimestampModel):
    total_data_sources: Optional[int]

class TokenValidationRequest(SQLModel):
    bh_github_token_url: str = None
    bh_github_username: str = None
    bh_github_provider: int = None
    bh_github_url: HttpUrl = None
    init_vector: str

class PreConfigureZoneBase(SQLModel):
    pre_configure_id: int = Field(default=None, primary_key=True)
    bronze_zone: str = Field(default=None, description="Name of the zone")
    silver_zone: str = Field(default=None, description="Name of the zone")
    gold_zone: str = Field(default=None, description="Name of the zone")
    log_zone: str = Field(default=None, description="Name of the zone")
    quarantine_zone: str = Field(default=None, description="Name of the zone")

    # Foreign Keys
    bh_env_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id")

class PreConfigureZone(PreConfigureZoneBase, TimestampModel, table=True):
    __tablename__ = "pre_configure_zone"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    project_environment: ProjectEnvironment = Relationship(back_populates="pre_configure_zone")

class PreConfigureZoneCreate(SQLModel):
    bronze_zone: str = None
    silver_zone: str = None
    gold_zone: str = None
    log_zone: str = None
    quarantine_zone: str = None
    bh_env_id: int = None

class PreConfigureZoneUpdate(SQLModel):
    bronze_zone: Optional[str] = None
    silver_zone: Optional[str] = None
    gold_zone: Optional[str] = None
    log_zone: Optional[str] = None
    quarantine_zone: Optional[str] = None

class PreConfigureZoneReturn(PreConfigureZoneBase, TimestampModel):
    pass

class PreConfigureZoneResponse(SQLModel):
    bronze_zone: str
    silver_zone: str
    gold_zone: str
    log_zone: str
    quarantine_zone: str

class ConfigureLifecycleBase(SQLModel):
    configure_lifecycle_id : int = Field(default=None, primary_key=True)
    std_bronze_zone: int = Field(default=None, description="Name of the zone")
    std_silver_zone: int = Field(default=None, description="Name of the zone")
    std_gold_zone: int = Field(default=None, description="Name of the zone")
    std_log_zone: int = Field(default=None, description="Name of the zone")
    std_quarantine_zone: int = Field(default=None, description="Name of the zone")
    arc_bronze_zone: int = Field(default=None, description="Name of the zone")
    arc_silver_zone: int = Field(default=None, description="Name of the zone")
    arc_gold_zone: int = Field(default=None, description="Name of the zone")
    arc_log_zone: int = Field(default=None, description="Name of the zone")
    arc_quarantine_zone: int = Field(default=None, description="Name of the zone")

    # Foreign Keys
    bh_env_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id")

class ConfigureLifecycle(ConfigureLifecycleBase, TimestampModel, table=True):
    __tablename__ = "configure_lifecycle"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    project_environment: ProjectEnvironment = Relationship(back_populates="configure_lifecycle")

class ConfigureLifecycleCreate(SQLModel):
    std_bronze_zone: int = None
    std_silver_zone: int = None
    std_gold_zone: int = None
    std_log_zone: int = None
    std_quarantine_zone: int = None
    arc_bronze_zone: int = None
    arc_silver_zone: int = None
    arc_gold_zone: int = None
    arc_log_zone: int = None
    arc_quarantine_zone: int = None
    bh_env_id: int = None

class ConfigureLifecycleUpdate(SQLModel):
    std_bronze_zone: Optional[int] = None
    std_silver_zone: Optional[int] = None
    std_gold_zone: Optional[int] = None
    std_log_zone: Optional[int] = None
    std_quarantine_zone: Optional[int] = None
    arc_bronze_zone: Optional[int] = None
    arc_silver_zone: Optional[int] = None
    arc_gold_zone: Optional[int] = None
    arc_log_zone: Optional[int] = None
    arc_quarantine_zone: Optional[int] = None

class ConfigureLifecycleReturn(ConfigureLifecycleBase, TimestampModel):
    pass


class FlowConnectionBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    connection_id : str = Field(default=None, description="Id of the env connection")
    connection_type: FlowConnectionType = Field(default=None, nullable=False, description="Type of the connection")
    connection_description: Optional[str] = Field(default=None, nullable=True, description="Description of the zone")

    # Foreign Keys
    bh_env_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.project_environment.bh_env_id")

class FlowConnection(FlowConnectionBase, TimestampModel, table=True):
    __tablename__ = "flow_connection"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    project_environment: ProjectEnvironment = Relationship(back_populates="flow_connection")

class FlowConnectionCreate(SQLModel):
    connection_id : str = None
    connection_type: FlowConnectionType = None
    connection_description: Optional[str] = None
    bh_env_id: Optional[int] = None

class FlowConnectionUpdate(SQLModel):
    connection_id : Optional[str] = None
    connection_type: Optional[FlowConnectionType] = None
    connection_description: Optional[str] = None


class FlowConnectionReturn(FlowConnectionBase, TimestampModel):
    pass