import json
import os
from time import sleep
from typing import Any, Tuple

from google.api_core.exceptions import NotFound, RetryError, ServiceUnavailable
from google.cloud import secretmanager
from google.oauth2 import service_account
from app.core.context import Context
from app.exceptions import BHGCPClientError
from app.services.base import BaseService
from app.core.config import Config
import logging

logger = logging.getLogger(__name__)


class GCPService(BaseService):
    def __init__(self, context: Context):
        super().__init__(context)

        self._secrets = None

    @property
    def secrets(self) -> 'GCPSecretsService':
        if self._secrets is None:
            self._secrets = GCPSecretsService(self.context)
        return self._secrets


class GCPSecretsService(BaseService):
    def __init__(self, context: Context):
        super().__init__(context)
        
        secrets_dir = '/etc/gcp/'
        # This will read the first file that ends with .json in the directory
        credentials_file = None
        for file_name in os.listdir(secrets_dir):
            logger.info(f"File name: {file_name}")
            if file_name.endswith('.json'):  
                credentials_file = os.path.join(secrets_dir, file_name)
                break

        if credentials_file is None:
            logger.error("No JSON credentials file found in the secrets directory.")
            raise FileNotFoundError("No JSON credentials file found in the secrets directory.")
   
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        self._secrets_client = secretmanager.SecretManagerServiceClient(credentials=credentials)

    async def get_secret(
            self,
            secret_name: str,
            project_id: str = Config.GOOGLE_CLOUD_PROJECT,
            retry: int = 3,
    ) -> dict | str:
        try:
            logger.info(f"Getting secret: {secret_name}")
            secret_path = self._secrets_client.secret_path(project_id, secret_name)
            version_path = secret_path + '/versions/latest'
            secret_version = self._secrets_client.access_secret_version(request={'name': version_path})
            secret_value = secret_version.payload.data.decode('utf-8')
            try:
                secret_value = json.loads(secret_value)
            except json.JSONDecodeError:
                pass
            return secret_value
        except (ServiceUnavailable, RetryError) as e:
            if retry > 0:
                sleep(10)
                return await self.get_secret(secret_name, project_id, retry - 1)
            else:
                logger.error(f"Failed to get secret: {secret_name}")
                raise BHGCPClientError(context={
                    'service': 'Secret Manager',
                    'project_nbr': project_id,
                    'error_code': 503,
                }) from e

    async def new_secret(
            self,
            secret_name: str,
            data: str,
            project_id: str = Config.GOOGLE_CLOUD_PROJECT,
    ) -> Tuple[Any, Any]:
        logger.info(f"Creating new secret: {secret_name}")
        project_path = f'projects/{project_id}'
        # Check if secret exists else create new one
        secret_path = self._secrets_client.secret_path(project_id, secret_name)
        try:
            logger.info(f"Checking if secret exists else create new one")
            secret = self._secrets_client.get_secret(request={'name': secret_path})
        except NotFound:
            logger.info(f"Secret does not exist. Creating new one")
            secret = self._secrets_client.create_secret(
                request={
                    'parent': project_path,
                    'secret_id': secret_name,
                    'secret': {
                        'replication': {'user_managed': {'replicas': [{'location': Config.PROJECT_LOCATION}]}},
                        'labels': {
                            'dnb_environment': str(Config.ENVIRONMENT),
                            'service': 'secretsmanager',
                            'name': 'bh-api'
                        },
                    },
                },
            )
        # Create new version with latest data payload
        version = self._secrets_client.add_secret_version(
            request={'parent': secret_path, 'payload': {'data': data.encode()}},
        )
        logger.info(f"Secret created: {version.name}")
        return secret, version.name

    async def delete_secret(
            self,
            secret_name: str,
            project_id: str = Config.GOOGLE_CLOUD_PROJECT,
    ) -> None:
        logger.info(f"Deleting secret: {secret_name}")
        secret_path = self._secrets_client.secret_path(project_id, secret_name)
        self._secrets_client.delete_secret(request={'name': secret_path})
