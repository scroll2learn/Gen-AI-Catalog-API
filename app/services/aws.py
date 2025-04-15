import os
from app.core.config import Config
from app.core.context import Context
from app.exceptions.aws import AWSSecretsClientError, AwsSecretkeyNotFoundError
import boto3
import time
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException
from google.cloud import storage
from databricks import sql

from app.models.aws import (
    QueryResult, 
    QueryRequest, 
    AWSCredentials, 
    ConnectionTestResponse,
    BucketModel, 
    SnowflakeCredentials,
    GCSCredentials,
    BigQueryCredentials,
    DatabricksCredentials
)
from app.services.base import BaseService
import snowflake.connector
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Any, Tuple
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AthenaQueryService(BaseService):
    model: QueryRequest = QueryRequest
    create_model: QueryResult = QueryResult

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, database: str, output_bucket: str):
        self.athena_client = boto3.client(
            'athena',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.database = database
        self.output_bucket = output_bucket

    def run_athena_query(self, query: str) -> str:
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={'OutputLocation': self.output_bucket},
        )
        return response['QueryExecutionId']

    def get_query_results(self, query_execution_id: str) -> QueryResult:
        while True:
            response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            if status == 'SUCCEEDED':
                break
            elif status in ['FAILED', 'CANCELLED']:
                raise HTTPException(status_code=500, detail=f"Query failed or was cancelled with status: {status}")
            time.sleep(1)

        response = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)
        result_data = response['ResultSet']
        columns = [col['Label'] for col in result_data['ResultSetMetadata']['ColumnInfo']]
        rows = [[col.get('VarCharValue') for col in row['Data']] for row in result_data['Rows'][1:]]  # Skip the header row

        return QueryResult(columns=columns, rows=rows)


class TestConnectionService(BaseService):
    model: AWSCredentials = AWSCredentials
    create_model: ConnectionTestResponse = ConnectionTestResponse

    async def test_aws_connection(self, credentials: AWSCredentials) -> ConnectionTestResponse:
        logger.info('Testing AWS connection with credentials: %s', credentials)
        try:
            session = boto3.Session(
                aws_access_key_id=credentials.aws_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key
            )
            s3_client = session.client('s3')
            response = s3_client.list_buckets()
            buckets = [BucketModel(name=bucket['Name']) for bucket in response['Buckets']]
            logger.info('AWS connection successful, buckets: %s', buckets)
            return ConnectionTestResponse(status="Connection successful", buckets=buckets)
        except NoCredentialsError:
            logger.error('No credentials found.')
            raise HTTPException(status_code=401, detail="No credentials found. Please configure your AWS credentials.")
        except PartialCredentialsError:
            logger.error('Incomplete credentials found.')
            raise HTTPException(status_code=401, detail="Incomplete credentials found. Please check your AWS credentials.")
        except Exception as e:
            logger.error('Error testing AWS connection: %s', e)
            raise HTTPException(status_code=500, detail=f"Invalid credentials: {str(e)}")


class SnowflakeConnectionTestService(BaseService):
    model: SnowflakeCredentials = SnowflakeCredentials
    create_model: ConnectionTestResponse = ConnectionTestResponse

    async def test_snowflake_connection(self, credentials: SnowflakeCredentials) -> ConnectionTestResponse:
        logger.info('Testing Snowflake connection with credentials: %s', credentials)
        try:
            conn = snowflake.connector.connect(
                user=credentials.user,
                password=credentials.password,
                account=credentials.account,
                warehouse=credentials.warehouse,
                database=credentials.database,
                schema=credentials.schema
            )
            cursor = conn.cursor()
            cursor.execute("SELECT CURRENT_VERSION()")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            logger.info('Snowflake connection successful, version: %s', result[0])
            return ConnectionTestResponse(status="Connection successful", version=result[0])
        except snowflake.connector.errors.ProgrammingError as e:
            logger.error('Error connecting to Snowflake: %s', e)
            raise HTTPException(status_code=401, detail="Connection failed. Please check your Snowflake credentials.")
        except Exception as e:
            logger.error('Error testing Snowflake connection: %s', e)
            raise HTTPException(status_code=500, detail=f"Connection failed with error: {str(e)}")


class GCSConnectionTestService(BaseService):
    model: GCSCredentials = GCSCredentials
    create_model: ConnectionTestResponse = ConnectionTestResponse

    async def test_gcs_connection(self, credentials: GCSCredentials):
        print('*************************************')
        print(credentials)
        try:
            # Create a client using the provided credentials
            client = storage.Client(
                project=credentials.project_id,
                credentials=service_account.Credentials.from_service_account_info({
                    "type": "service_account",
                    "project_id": credentials.project_id,
                    "private_key_id": "",
                    "private_key": credentials.private_key,
                    "client_email": credentials.client_email,
                    "client_id": "",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": ""
                })
            )

            # List buckets to verify connection
            buckets = list(client.list_buckets())
            bucket_names = [bucket.name for bucket in buckets]
            print('Connection successful, Buckets:', bucket_names)

            return ConnectionTestResponse(status="Connection successful", buckets=bucket_names)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Connection failed with error: {str(e)}")
        
    
class BigQueryConnectionTestService(BaseService):
    model: BigQueryCredentials = BigQueryCredentials
    create_model: ConnectionTestResponse = ConnectionTestResponse

    async def test_bigquery_connection(self, credentials: BigQueryCredentials):
        print('*************************************')
        print(credentials)
        try:
            # Create a client using the provided credentials
            credentials_info = {
                "type": "service_account",
                "project_id": credentials.project_id,
                "private_key_id": "",
                "private_key": credentials.private_key,
                "client_email": credentials.client_email,
                "client_id": "",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": ""
            }

            credentials_obj = service_account.Credentials.from_service_account_info(credentials_info)

            client = bigquery.Client(
                project=credentials.project_id,
                credentials=credentials_obj
            )

            # Execute a simple query to verify connection
            query = "SELECT 1"
            query_job = client.query(query)
            results = query_job.result()
            print('Connection successful, Query results:', results)
            
            return ConnectionTestResponse(status="Connection successful", results=[row for row in results])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Connection failed with error: {str(e)}")
        
        
class DatabricksConnectionTestService(BaseService):
    model: DatabricksCredentials = DatabricksCredentials
    create_model: ConnectionTestResponse = ConnectionTestResponse

    async def test_databricks_connection(self, credentials: DatabricksCredentials):
        print('*************************************')
        print(credentials)
        try:
            # Establish a connection to Databricks
            connection = sql.connect(
                server_hostname=credentials.server_hostname,
                http_path=credentials.http_path,
                access_token=credentials.access_token
            )

            # Execute a simple query to verify connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            print('Connection successful, Query results:', results)
            
            return ConnectionTestResponse(status="Connection successful", results=results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Connection failed with error: {str(e)}")

class AWSService(BaseService):
    def __init__(self, context: Context):
        super().__init__(context)
        self._secrets = None

    @property
    def secrets(self) -> 'AWSSecretsService':
        if self._secrets is None:
            self._secrets = AWSSecretsService(self.context)
        return self._secrets
    
    @property
    def buckets(self) -> 'AWSS3Service':
        if self._buckets is None:
            self._buckets = AWSS3Service(self.context)
        return self._buckets

class AWSSecretsService(BaseService):
    '''
    AWS Secrets Manager service.
    '''
    def __init__(self, context: Context):
        super().__init__(context)
        # Check if AWS keys are provided
        if not Config.AWS_ACCESS_KEY or not Config.AWS_SECRET_ACCESS_KEY:
            raise AwsSecretkeyNotFoundError()
        
        self._secrets_client = boto3.client(
            'secretsmanager',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )

    async def new_secret(
            self,
            secret_name: str,
            secret_data: str
    ) -> Tuple[str, str]:

        try:
            # Check if the secret already exists
            try:
                existing_secret = self._secrets_client.describe_secret(SecretId=secret_name)
                version_ids_to_stages = existing_secret['VersionIdsToStages']
                latest_version_id = next(iter(version_ids_to_stages.keys()))  # Get the first (latest) version ID
                logger.info(f"Secret {secret_name} already exists. Current version ID: {latest_version_id}")
                return existing_secret['ARN'], existing_secret['Name']
            except self._secrets_client.exceptions.ResourceNotFoundException:
                # Create a new secret if it doesn't exist
                logger.info(f"Creating new secret: {secret_name}")
                response = self._secrets_client.create_secret(
                    Name=secret_name,
                    SecretString=secret_data,
                    Tags=[
                        {'Key': 'dnb_environment', 'Value': Config.ENVIRONMENT},
                        {'Key': 'service', 'Value': 'secretsmanager'},
                        {'Key': 'name', 'Value': 'bh-api'},
                    ]
                )
                logger.info(f"Secret created: {response['ARN']}")
                return response['ARN'], response['Name']

        except ClientError as e:
            logger.error(f"Failed to create or update secret: {e}")
            raise
    
    async def get_secret(self, secret_name: str) -> dict:
        try:
            response = self._secrets_client.get_secret_value(SecretId=secret_name)
            secret_data = response['SecretString']
            return json.loads(secret_data)
        except self._secrets_client.exceptions.ResourceNotFoundException as e:
            logger.error(f"Secret {secret_name} not found.")
            raise AWSSecretsClientError(
                context={"message": str(e)}
            )
        except ClientError as e:
            logger.error(f"Failed to retrieve secret: {e}")
            raise AWSSecretsClientError(
                context={"message": str(e)}
            )

    async def delete_secret(self, secret_name: str) -> str:
        try:
            response = self._secrets_client.delete_secret(
                SecretId=secret_name,
                ForceDeleteWithoutRecovery=True
            )
            logger.info(f"Secret {secret_name} permanently deleted.")

            return response['ARN']

        except self._secrets_client.exceptions.ResourceNotFoundException:
            logger.error(f"Secret {secret_name} not found.")
            raise AWSSecretsClientError(
                context={"message": f"Secret {secret_name} not found."}
            )
        except ClientError as e:
            logger.error(f"Failed to delete secret: {e}")
            raise AWSSecretsClientError(
                context={"message": str(e)}
            )


class AWSS3Service:
    '''
    AWS S3 service.
    '''
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str = Config.AWS_REGION):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def create_bucket(self, bucket_name: str) -> None:
        try:
            # Check if the region is 'us-east-1'
            if Config.AWS_REGION == 'us-east-1':
                # Create bucket without LocationConstraint for us-east-1
                response = self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                # Add LocationConstraint for other regions
                response = self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': 'eu-east-1'}
                )
            logger.info(f"Bucket {bucket_name} created successfully.")
        except ClientError as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")
            raise

    def upload_json_to_bucket(self, bucket_name: str, file_name: str, json_data: dict) -> None:
        try:
            json_content = json.dumps(json_data)
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json_content,
                ContentType='application/json'
            )
            logger.info(f"File {file_name} uploaded to bucket {bucket_name}.")
        except ClientError as e:
            logger.error(f"Failed to upload file {file_name} to bucket {bucket_name}: {e}")
            raise

    def create_bucket_and_upload_json(self, bucket_name: str, file_name: str, json_data: dict) -> None:
        self.create_bucket(bucket_name)
        self.upload_json_to_bucket(bucket_name, file_name, json_data)
    
    def upload_file_to_s3(self, bucket_name, key, file_content, content_type):
        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=file_content,
            ContentType=content_type,
        )


class AWSMWAAService:
    """
    AWS MWAA service for interacting with Managed Workflows for Apache Airflow.
    """

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str = Config.AWS_REGION):
        """
        Initialize the MWAA client with AWS credentials and region.
        """
        self.mwaa_client = boto3.client(
            'mwaa',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def create_environment(self, environment_name: str, bucket_name: str) -> None:
        """
        Create a new MWAA environment.

        :param environment_name: The name of the environment to create.
        :param execution_role: The ARN of the execution role for the environment.
        :param bucket_name: The S3 bucket name used for DAGs and plugins.
        """
        try:
            response = self.mwaa_client.create_environment(
                Name=environment_name,
                ExecutionRoleArn='arn:aws:iam::123456789012:role/newnew',
                SourceBucketArn='arn:aws:s3:::my-valid-bucket-name',
                DagS3Path='dags',
                PluginsS3Path='plugins',
                AirflowVersion='2.5.1',
                EnvironmentClass='mw1.small',
                MaxWorkers=2,
                NetworkConfiguration={
                    'SecurityGroupIds': ['sg-0123456789abcdef0'],  
                    'SubnetIds': ['subnet-0123456789abcdef0', 'subnet-abcdef0123456789']  
                }
            )
            logger.info(f"Environment {environment_name} created successfully. Status: {response['ResponseMetadata']['HTTPStatusCode']}")
        except ClientError as e:
            logger.error(f"Failed to create environment {environment_name}: {e}")
            raise


    def list_environments(self) -> list[str]:
        """
        List all MWAA environments in the account and region.

        :return: List of environment names.
        """
        try:
            response = self.mwaa_client.list_environments()
            environments = response.get('Environments', [])
            logger.info(f"Retrieved MWAA environments: {environments}")
            return environments
        except ClientError as e:
            logger.error(f"Failed to list MWAA environments: {e}")
            raise

    def get_environment_by_name(self, environment_name: str) -> dict:
        """
        Retrieve details for a specific MWAA environment.

        :param environment_name: Name of the MWAA environment.
        :return: Dictionary containing environment details.
        """
        try:
            response = self.mwaa_client.get_environment(Name=environment_name)
            environment_details = response.get('Environment', {})
            logger.info(f"Retrieved details for environment '{environment_name}': {environment_details}")
            return environment_details
        except ClientError as e:
            logger.error(f"Failed to get details for environment '{environment_name}': {e}")
            raise
