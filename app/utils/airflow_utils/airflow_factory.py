from app.core.context import Context
from app.utils.airflow_utils.aws_airflow import AWSAirflowService
# from app.utils.cloud_services.gcp_servicesimport GCPCloudService

from app.utils.cloud_service_utils import get_cloud_decrypted_secrets

class AirflowFactory:

    @staticmethod
    async def get_airflow_service(cloud_type: str, bh_env_name: str, ctx: Context, airflow_env_name: str = None, region_name: str = "us-east-1"):
        if cloud_type == "aws":
            access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env_name, ctx=ctx)
            return AWSAirflowService(access_key, secret_access_key, region_name, airflow_env_name)
        elif cloud_type == "gcp":
            raise NotImplementedError("GCP not implemented")
            # return GCPCloudService(env_name)
        else:
            raise ValueError("Invalid cloud type")
        
    @staticmethod
    async def get_airflow_mwaa_env(cloud_type: str, access_key: str, secret_access_key: str, region_name: str = "us-east-1"):
        if cloud_type == "aws":
            return AWSAirflowService(access_key, secret_access_key, region_name)
        elif cloud_type == "gcp":
            raise NotImplementedError("GCP not implemented")
            # return GCPCloudService(env_name)
        else:
            raise ValueError("Invalid cloud type")