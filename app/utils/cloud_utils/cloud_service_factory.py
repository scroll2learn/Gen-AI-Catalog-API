from app.utils.cloud_utils.aws_services import AWSCloudService
# from app.utils.cloud_services.gcp_servicesimport GCPCloudService

from app.utils.cloud_service_utils import get_cloud_decrypted_secrets

class CloudServiceFactory:

    @staticmethod
    async def get_cloud_service(cloud_type: str, env_name: str, region_name: str = "us-east-1"):
        if cloud_type == "aws":
            access_key, secret_access_key = await get_cloud_decrypted_secrets(env_name)
            return AWSCloudService(access_key, secret_access_key, region_name)
        elif cloud_type == "gcp":
            raise NotImplementedError("GCP not implemented")
            # return GCPCloudService(env_name)
        else:
            raise ValueError("Invalid cloud type")
