import boto3
import logging
from app.utils.cloud_utils.cloud_service import CloudService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSCloudService(CloudService):

    def __init__(self, access_key, secret_access_key, region_name: str):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region_name = region_name

        # Create a boto3 session
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )

    async def copy_file_to_object_storage(self, bucket_name: str, file_path: str, object_name: str):
        """
        Copy a file to an S3 bucket
        """
        s3_client = self.session.client('s3')

        try:
            response = s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded to S3 bucket: {bucket_name}")
            return response
        except Exception as e:
            logger.error(f"Error uploading file to S3 bucket: {bucket_name}")
            logger.error(e)
            raise e
