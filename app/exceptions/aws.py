from fastapi import status
from app.exceptions import BaseHTTPException

class AWSSecretsClientError(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = 'AWS_SECRETS_MANAGER_CLIENT_ERROR'
    message = 'AWS Secrets Manager Client Error: {message}'


class AwsSecretkeyNotFoundError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 'AWS_SECRET_KEY_NOT_FOUND'
    message = 'AWS Secret Key Not Found'


class AwsSecretkeyInvalidError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 'AWS_SECRET_KEY_INVALID'
    message = 'AWS Secret Key Invalid'


class MwaaEnvironmentNotFoundError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 'MWAA_ENVIRONMENT_NOT_FOUND'
    message = 'MWAA Environment {env_name} Not Found'

class AWSCredentialsNotFoundError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = 'AWS_CREDENTIALS_NOT_FOUND'
    message = 'AWS Credentials Not Found for local docker environment'
