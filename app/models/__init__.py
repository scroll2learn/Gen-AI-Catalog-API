from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import Config

Base = declarative_base(metadata=MetaData(schema=Config.DB_SCHEMA))


"""
    Registering Tables in the database
"""

from .codes_hdr import CodesHdr,CodesDtl
from .app_user import AppUser
from .bh_project import BHProject, LakeZone, ProjectEnvironment, ConfigureLifecycle, PreConfigureZone
from .bh_user import BHUser
from .platform_region import PlatformRegion
from .data_source import DataSource, DataSourceMetadata
from .data_source_layout import DataSourceLayout
from .layout_fields import LayoutFields
from .fld_dq_types import FieldDQTypes
from .layout_fields_dq import LayoutFieldsDQ
from .function_registry import FunctionRegistry
from .joins import Joins, JoinOn
from .pipelines import Pipeline, PipelineDefinition, PipelineValidationError, PipelineConfig, PipelineVersion, PipelineConnection
from .transform_logic import TransformLogic, TransformInputFields, TransformOutputFields
from .customer import Customer,ConnectionDtl
from .fld_properties import FieldProperties
from .bh_audit import AuditEvents
from .fld_recommendations import FieldRecommendations
from .pulish_data import PublishDetails
from .aws import AWSCredentials,SnowflakeCredentials
from .connection_registry import ConnectionRegistry, ConnectionConfig
from .flow import Flow
from .schema import Schema
from .release_bundle import BHReleaseBundle