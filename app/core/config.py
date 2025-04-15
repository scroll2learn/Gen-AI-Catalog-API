import os
from typing import Any, Callable, List, Optional, Union

from dotenv import load_dotenv

from sqlalchemy.engine.url import URL

class ConfigHelper:
    def __init__(
            self,
            use_secrets: bool,
            region: Optional[str] = None,
    ):
        if use_secrets:
            self._config_dict = None # To be Updated
        else:
            self._config_dict = {}
        self.region = region

    def get(self, key: str, default: Any = None, *, factory: Callable[[Any], Any] = None) -> Any:
        value = self._config_dict.get(key, os.getenv(key))

        if value is None:
            value = default
        
        return value
    
    @staticmethod
    def parse_list(delimiter: str = ','):
        def inner(value: Union[str, List]):
            if isinstance(value, list):
                return value
            return value.split(delimiter)
        return inner

class Config:
    load_dotenv(verbose=True)

    # Cloud Variables
    CLOUD_SECRET: str = None #os.getenv('CLOUD_SECRET')
    CLOUD_REGION: str = None #os.getenv('CLOUD_REGION')

    cfg = ConfigHelper(CLOUD_SECRET, CLOUD_REGION)

    # API Variables
    API_HOST: str = cfg.get('API_HOST', default='0.0.0.0')
    API_PORT: str = cfg.get('API_PORT', default='5432')
    API_LOG_LEVEL: str = cfg.get('API_LOG_LEVEL', default='info')

    # Author Data Endppoint
    AUTHOR_DATA_ENDPOINT: str = cfg.get('AUTHOR_BASE_URL')
    GITHUB_PROVIDER_BASE_URL: str = cfg.get('GITHUB_PROVIDER_BASE_URL')
    GITLAB_PROVIDER_BASE_URL: str = cfg.get('GITLAB_PROVIDER_BASE_URL')
    AZURE_REPOS_PROVIDER_BASE_URL: str = cfg.get('AZURE_REPOS_PROVIDER_BASE_URL')
    BITBUCKET_PROVIDER_BASE_URL: str = cfg.get('BITBUCKET_PROVIDER_BASE_URL')

    CORS_ALLOW_ORIGINS: List = cfg.get('CORS_ALLOW_ORIGINS', default=['*'], factory=ConfigHelper.parse_list())

    SQLALCHEMY_DATABASE_URI: URL = URL(
        drivername='postgresql+asyncpg',
        username=cfg.get('POSTGRES_USER'),
        password=cfg.get('POSTGRES_PASSWORD'),
        host=cfg.get('POSTGRES_HOST', 'localhost'),
        port=cfg.get('POSTGRES_PORT', '5432'),
        database=cfg.get('POSTGRES_DB'),
        query={},
    )

    CLOUD_TYPE: str = cfg.get('CLOUD_TYPE', default='AWS')
    ENVIRONMENT: str = cfg.get('ENVIRONMENT')
    DB_SCHEMA: str = cfg.get('DB_SCHEMA', default='catalogdb')

    CONNECTOR_PREFIX: str = cfg.get('CONNECTOR_PREFIX', 'bh')
    DECRYPTION_KEY: str = cfg.get('DECRYPTION_KEY')

    # Only for local BH development (This keys are for BH Project)
    # This is not needed for K8's as it will be role based access
    GOOGLE_CLOUD_PROJECT: str = cfg.get('GOOGLE_CLOUD_PROJECT')
    PROJECT_LOCATION: str = cfg.get('PROJECT_LOCATION')
    GOOGLE_APPLICATION_CREDENTIALS_JSON: str = cfg.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')


    # Only for local BH development (This keys are for BH Project)
    # This is not needed for K8's as it will be role based access
    AWS_REGION: str = cfg.get('AWS_REGION')
    AWS_ACCESS_KEY: str = cfg.get('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY: str = cfg.get('AWS_SECRET_ACCESS_KEY')
    TOKEN: str = cfg.get('TOKEN')
    OWNER: str = cfg.get('OWNER')
    REPO: str = cfg.get('REPO')
    CELERY_BROKER_PASSWORD: str = cfg.get('CELERY_BROKER_PASSWORD')
    BH_APP_BUCKET: str = cfg.get('BH_APP_BUCKET')
    SCHEMA_FILE_PATH: str = cfg.get('SCHEMA_FILE_PATH')
    BH_AI_AGENT_URL: str = cfg.get('BH_AI_AGENT_URL')
    BH_MONITER_URL: str = cfg.get('BH_MONITER_URL')
    PIPELINE_ENGINE_VERSION: str = cfg.get('PIPELINE_ENGINE_VERSION')
