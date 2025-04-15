from app.db.base import AsyncSessionLocal
from app.core.config import Config

class Context:
    def __init__(self):
        self._db_session = None
        self._staging_registry_parameter_service = None
        self._bh_project_service = None
        self._lake_zone_service = None
        self._data_source_service = None
        self._data_source_mtd_service = None
        self._data_source_layout_service = None
        self._layout_fields_service = None
        self._layout_fields_dq_service = None
        self._fields_dq_types_service = None
        self._bh_user_service = None
        self._app_user_service = None
        self._codes_dtl_service = None
        self._codes_hdr_service = None
        self._platform_region_service = None
        self._function_registry_service = None
        self._join_service = None
        self._join_on_service = None
        self._pipeline_service = None
        self._pipeline_src_service = None
        self._pipeline_tgt_service = None
        self._transform_logic_service = None
        self._transform_input_service = None
        self._transform_output_service = None
        self._engine_integrations_service = None
        self._customer_service = None
        self._connection_dtl_service = None
        self._field_properties_service = None
        self._field_recommendations_service = None
        self._test_connection_service = None
        self._publish_details_service = None
        self._publish_query_details_service = None
        self._athena_query_service=None
        self._test_snowflake_connection_service=None
        self._test_gcs_connection_service=None
        self._test_bigquery_connection_service=None
        self._test_databricks_connection_service=None
        self._project_environment_service=None
        self._connection_registry=None
        self._gcp_service=None
        self._connection_config_service=None
        self._aws_service=None
        self._flow_service = None
        self._schedule_interval_service = None
        self._pre_configure_zone_service = None
        self._configure_lifecycle_service = None
        self._flow_connection_service = None
        self._flow_deployment_service = None
        self._pipeline_setting_service = None
        self._pipeline_definition_service = None
        self._pipeline_config_service = None
        self._pipeline_version_service = None
        self._schema_service = None
        self._flow_defination_service = None
        self._flow_version_service = None
        self._flow_config_service = None
        self._user_detail_service = None
        self._release_bundle_service = None
        self._pipeline_connection_service = None
        self._pipeline_parameter_service = None
        
    async def __aenter__(self):
        # Create a new AsyncSession instance when entering the context
        self._db_session = AsyncSessionLocal()
        await self._db_session.execute(f"SET search_path TO {Config.DB_SCHEMA}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # exc_type: The type of exception raised within the async with block, 
           # if any. If no exception was raised, this will be None.
        # exc_val: The value of the exception raised, if any. 
           # This is the exception instance itself. If no exception was raised, this will be None.
        # exc_tb: The traceback object associated with the exception, 
            # if an exception was raised. This provides stack trace information that can be used for debugging. 
            # If no exception was raised, this will be None.
        if exc_type is not None or exc_val is not None or exc_tb is not None:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
        # Close the session when exiting the context
        await self._db_session.close()

    @property
    def db_session(self):
        # This property now simply returns the session without being async
        return self._db_session
    
    def set_db_session(self, session):
        self._db_session = session
    
    @property
    def bh_project_service(self) -> 'BHProjectService':
        # Lazy initialization of the service
        if self._bh_project_service is None:
            self._bh_project_service = BHProjectService(self)
        return self._bh_project_service
    
    @property
    def lake_zone_service(self) -> 'LakeZoneService':
        # Lazy initialization of the service
        if self._lake_zone_service is None:
            self._lake_zone_service = LakeZoneService(self)
        return self._lake_zone_service
    
    @property
    def data_source_service(self) -> 'DataSourceService':
        # Lazy initialization of the service
        if self._data_source_service is None:
            self._data_source_service = DataSourceService(self)
        return self._data_source_service
    
    @property
    def data_source_mtd_service(self) -> 'DataSourceMetadataService':
        # Lazy initialization of the service
        if self._data_source_mtd_service is None:
            self._data_source_mtd_service = DataSourceMetadataService(self)
        return self._data_source_mtd_service

    @property
    def data_source_layout_service(self) -> 'DataSourceLayoutService':
        # Lazy initialization of the service
        if self._data_source_layout_service is None:
            self._data_source_layout_service = DataSourceLayoutService(self)
        return self._data_source_layout_service
    
    @property
    def layout_fields_service(self) -> 'LayoutFieldsService':
        # Lazy initialization of the service
        if self._layout_fields_service is None:
            self._layout_fields_service = LayoutFieldsService(self)
        return self._layout_fields_service

    @property
    def layout_fields_dq_service(self) -> 'LayoutFieldsDQService':
        # Lazy initialization of the service
        if self._layout_fields_dq_service is None:
            self._layout_fields_dq_service = LayoutFieldsDQService(self)
        return self._layout_fields_dq_service

    @property
    def fields_dq_types_service(self) -> 'FieldDQTypesService':
        # Lazy initialization of the service
        if self._fields_dq_types_service is None:
            self._fields_dq_types_service = FieldDQTypesService(self)
        return self._fields_dq_types_service

    @property
    def bh_user_service(self) -> 'BHUserService':
            # Lazy initialization of the service
            if self._bh_user_service is None:
                self._bh_user_service = BHUserService(self)
            return self._bh_user_service
    @property
    def app_user_service(self) -> 'AppUserService':
            # Lazy initialization of the service
            if self._app_user_service is None:
                self._app_user_service = AppUserService(self)
            return self._app_user_service

    @property
    def codes_hdr_service(self) -> 'CodesHdrService':
            # Lazy initialization of the service
            if self._codes_hdr_service is None:
                self._codes_hdr_service = CodesHdrService(self)
            return self._codes_hdr_service

    @property
    def codes_dtl_service(self) -> 'CodesDtlService':
            # Lazy initialization of the service
            if self._codes_dtl_service is None:
                self._codes_dtl_service = CodesDtlService(self)
            return self._codes_dtl_service

    @property
    def platform_region_service(self) -> 'PlatformRegionService':
            # Lazy initialization of the service
            if self._platform_region_service is None:
                self._platform_region_service = PlatformRegionService(self)
            return self._platform_region_service
    
    @property
    def function_registry_service(self) -> 'FunctionRegistryService':
            # Lazy initialization of the service
            if self._function_registry_service is None:
                self._function_registry_service = FunctionRegistryService(self)
            return self._function_registry_service

    @property
    def join_service(self) -> 'JoinsService':
            # Lazy initialization of the service
            if self._join_service is None:
                self._join_service = JoinsService(self)
            return self._join_service

    @property
    def join_on_service(self) -> 'JoinOnService':
            # Lazy initialization of the service
            if self._join_on_service is None:
                self._join_on_service = JoinOnService(self)
            return self._join_on_service

    @property
    def pipeline_service(self) -> 'PipelinesService':
            # Lazy initialization of the service
            if self._pipeline_service is None:
                self._pipeline_service = PipelinesService(self)
            return self._pipeline_service

    @property
    def pipeline_definition_service(self) -> 'PipelinesDefinitionService':
            # Lazy initialization of the service
            if self._pipeline_definition_service is None:
                self._pipeline_definition_service = PipelinesDefinitionService(self)
            return self._pipeline_definition_service
    
    @property
    def pipeline_version_service(self) -> 'PipelineVersionService':
            # Lazy initialization of the service
            if self._pipeline_version_service is None:
                self._pipeline_version_service = PipelineVersionService(self)
            return self._pipeline_version_service
    
    @property
    def pipeline_config_service(self) -> 'PipelineConfigService':
            # Lazy initialization of the service
            if self._pipeline_config_service is None:
                self._pipeline_config_service = PipelineConfigService(self)
            return self._pipeline_config_service

    @property
    def transform_logic_service(self) -> 'TransformLogicService':
            # Lazy initialization of the service
            if self._transform_logic_service is None:
                self._transform_logic_service = TransformLogicService(self)
            return self._transform_logic_service

    @property
    def transform_input_service(self) -> 'TransformInputFieldsService':
            # Lazy initialization of the service
            if self._transform_input_service is None:
                self._transform_input_service = TransformInputFieldsService(self)
            return self._transform_input_service

    @property
    def transform_output_service(self) -> 'TransformOutputFieldsService':
            # Lazy initialization of the service
            if self._transform_output_service is None:
                self._transform_output_service = TransformOutputFieldsService(self)
            return self._transform_output_service

    @property
    def engine_integrations_service(self) -> 'EngineConfigurationsService':
            # Lazy initialization of the service
            if self._engine_integrations_service is None:
                self._engine_integrations_service = EngineConfigurationsService(self)
            return self._engine_integrations_service
    
    @property
    def customer_service(self) -> 'CustomerService':
        # Lazy initialization of the service
        if self._customer_service is None:
            self._customer_service = CustomerService(self)
        return self._customer_service
    
    @property
    def test_connection_service(self) -> 'TestConnectionService':
        # Lazy initialization of the service
        if self._test_connection_service is None:
            self._test_connection_service = TestConnectionService(self)
        return self._test_connection_service
    
    @property
    def test_snowflake_connection_service(self) -> 'SnowflakeConnectionTestService':
        # Lazy initialization of the service
        if self._test_snowflake_connection_service is None:
            self._test_snowflake_connection_service = SnowflakeConnectionTestService(self)
        return self._test_snowflake_connection_service
    
    @property
    def test_gcs_connection_service(self) -> 'GCSConnectionTestService':
        # Lazy initialization of the service
        if self._test_gcs_connection_service is None:
            self._test_gcs_connection_service = GCSConnectionTestService(self)
        return self._test_gcs_connection_service
    
    @property
    def test_bigquery_connection_service(self) -> 'BigQueryConnectionTestService':
        # Lazy initialization of the service
        if self._test_bigquery_connection_service is None:
            self._test_bigquery_connection_service = BigQueryConnectionTestService(self)
        return self._test_bigquery_connection_service
    
    @property
    def test_databricks_connection_service(self) -> 'DatabricksConnectionTestService':
        # Lazy initialization of the service
        if self._test_databricks_connection_service is None:
            self._test_databricks_connection_service = DatabricksConnectionTestService(self)
        return self._test_databricks_connection_service
    
    
    @property
    def connection_dtl_service(self) -> 'ConnectionDtlService':
        # Lazy initialization of the service
        if self._connection_dtl_service is None:
            self._connection_dtl_service = ConnectionDtlService(self)
        return self._connection_dtl_service

    @property
    def field_properties_service(self) -> 'FieldPropertiesService':
        # Lazy initialization of the service
        if self._field_properties_service is None:
            self._field_properties_service = FieldPropertiesService(self)
        return self._field_properties_service
    
    @property
    def field_recommendations_service(self) -> 'FieldRecommendationsService':
        # Lazy initialization of the service
        if self._field_recommendations_service is None:
            self._field_recommendations_service = FieldRecommendationsService(self)
        return self._field_recommendations_service
    @property
    def publish_details_service(self) -> 'PublishDetailsService':
        # Lazy initialization of the service
        if self._publish_details_service is None:
            self._publish_details_service = PublishDetailsService(self)
        return self._publish_details_service
    
    @property
    def publish_query_details_service(self) -> 'PublishQueryDetailsService':
        # Lazy initialization of the service
        if self._publish_query_details_service is None:
            self._publish_query_details_service = PublishQueryDetailsService(self)
        return self._publish_query_details_service
    @property
    def athena_query_service(self) -> 'AthenaQueryService':
        # Lazy initialization of the service
        if self._athena_query_service is None:
            self._athena_query_service = AthenaQueryService(self)
        return self._athena_query_service
  
    @property
    def project_environment_service(self) -> 'ProjectEnvironmentService':
        # Lazy initialization of the service
        if self._project_environment_service is None:
            self._project_environment_service = ProjectEnvironmentService(self)
        return self._project_environment_service

    @property
    def connection_registry(self) -> 'ConnectionRegistryService':
        # Lazy initialization of the service
        if self._connection_registry is None:
            self._connection_registry = ConnectionRegistryService(self)
        return self._connection_registry
    
    @property
    def gcp_service(self) -> 'GCPService':
        # Lazy initialization of the service
        if self._gcp_service is None:
            self._gcp_service = GCPService(self)
        return self._gcp_service
    
    @property
    def connection_config_service(self) -> 'ConnectionConfigService':
        # Lazy initialization of the service
        if self._connection_config_service is None:
            self._connection_config_service = ConnectionConfigService(self)
        return self._connection_config_service

    @property
    def aws_service(self) -> 'AWSService':
        # Lazy initialization of the service
        if self._aws_service is None:
            self._aws_service = AWSService(self)
        return self._aws_service
    
    @property
    def flow_service(self) -> 'FlowService':
        # Lazy initialization of the service
        if self._flow_service is None:
            self._flow_service = FlowService(self)
        return self._flow_service
    

    @property
    def pre_configure_zone_service(self) -> 'PreConfigureZoneService':
        # Lazy initialization of the service
        if self._pre_configure_zone_service is None:
            self._pre_configure_zone_service = PreConfigureZoneService(self)
        return self._pre_configure_zone_service

    @property
    def configure_lifecycle_service(self) -> 'ConfigureLifecycleService':
        # Lazy initialization of the service
        if self._configure_lifecycle_service is None:
            self._configure_lifecycle_service = ConfigureLifecycleService(self)
        return self._configure_lifecycle_service
    
    @property
    def flow_connection_service(self) -> 'FlowConnectionService':
        # Lazy initialization of the service
        if self._flow_connection_service is None:
            self._flow_connection_service = FlowConnectionService(self)
        return self._flow_connection_service
    
    @property
    def flow_deployment_service(self) -> 'FlowDeploymentService':   
        # Lazy initialization of the service
        if self._flow_deployment_service is None:
            self._flow_deployment_service = FlowDeploymentService(self)
        return self._flow_deployment_service
    
    @property
    def pipeline_setting_service(self) -> 'PipelineSettingService': 
        # Lazy initialization of the service
        if self._pipeline_setting_service is None:
            self._pipeline_setting_service = PipelineSettingService(self)
        return self._pipeline_setting_service
    
    @property
    def user_detail_service(self) -> 'UserDetailService':
        # Lazy initialization of the service
        if self._user_detail_service is None:
            self._user_detail_service = UserDetailService(self)
        return self._user_detail_service
    
    @property
    def schema_service(self) -> 'SchemaService':
        # Lazy initialization of the service
        if self._schema_service is None:
            self._schema_service = SchemaService(self)
        return self._schema_service

    @property
    def flow_defination_service(self) -> 'FlowDefinitionService':
        # Lazy initialization of the service
        if self._flow_defination_service is None:
            self._flow_defination_service = FlowDefinitionService(self)
        return self._flow_defination_service
    
    @property
    def flow_version_service(self) -> 'FlowVersionService':
        # Lazy initialization of the service
        if self._flow_version_service is None:
            self._flow_version_service = FlowVersionService(self)
        return self._flow_version_service
    
    @property
    def flow_config_service(self) -> 'FlowConfigService':
        # Lazy initialization of the service
        if self._flow_config_service is None:
            self._flow_config_service = FlowConfigService(self)
        return self._flow_config_service
    
    @property
    def release_bundle_service(self) -> 'BHReleaseBundleService':
        # Lazy initialization of the service
        if self._release_bundle_service is None:
            self._release_bundle_service = BHReleaseBundleService(self)
        return self._release_bundle_service
    
    @property
    def pipeline_connection_service(self) -> 'PipelineConnectionService':
        # Lazy initialization of the service
        if self._pipeline_connection_service is None:
            self._pipeline_connection_service = PipelineConnectionService(self)
        return self._pipeline_connection_service

    @property
    def pipeline_parameter_service(self) -> 'PipelineParameterService':
        # Lazy initialization of the service
        if self._pipeline_parameter_service is None:
            self._pipeline_parameter_service = PipelineParameterService(self)
        return self._pipeline_parameter_service
    

# To Avoid Circular Imports added at the end
from app.services.bh_project import BHProjectService, LakeZoneService, ProjectEnvironmentService, PreConfigureZoneService, ConfigureLifecycleService, FlowConnectionService
from app.services.data_source import DataSourceService, DataSourceMetadataService
from app.services.data_source_layout import DataSourceLayoutService
from app.services.layout_fields import LayoutFieldsService
from app.services.layout_fields_dq import LayoutFieldsDQService
from app.services.fld_dq_types import FieldDQTypesService
from app.services.bh_user import BHUserService, UserDetailService
from app.services.app_user import AppUserService
from app.services.codes_hdr import CodesHdrService,CodesDtlService
from app.services.platform_region import PlatformRegionService
from app.services.function_registry import FunctionRegistryService
from app.services.joins import JoinsService, JoinOnService
from app.services.pipelines import PipelinesService, PipelinesDefinitionService, PipelineConfigService, PipelineVersionService, PipelineConnectionService, PipelineParameterService
from app.services.transform_logic import TransformLogicService, TransformInputFieldsService, TransformOutputFieldsService
from app.services.engine_integrations import EngineConfigurationsService
from app.services.customer import CustomerService, ConnectionDtlService
from app.services.fld_properties import FieldPropertiesService
from app.services.fld_recommendations import FieldRecommendationsService
from app.services.publish_data import PublishDetailsService,PublishQueryDetailsService
from app.services.aws import AthenaQueryService,TestConnectionService,SnowflakeConnectionTestService,GCSConnectionTestService,BigQueryConnectionTestService,DatabricksConnectionTestService, AWSService
from app.services.connection_registry import ConnectionRegistryService, ConnectionConfigService
from app.services.gcp import GCPService
from app.services.flow import FlowService, FlowDeploymentService, FlowDefinitionService, FlowVersionService, FlowConfigService
from app.services.schema import SchemaService
from app.services.release_bundle import BHReleaseBundleService
