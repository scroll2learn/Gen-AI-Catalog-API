from fastapi import status
from app.exceptions import BaseHTTPException


class PipelineAlreadyExists(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Pipeline already exists with name [{name}].'
    error_code = 'PIPELINE_ALREADY_EXISTS'

class PipelineNameAlphanumeric(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Pipeline name must contain only alphanumeric characters.'
    error_code = 'Pipeline_NAME_ALPHANUMERIC'

class PipelineDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Pipeline does not exist.'
    error_code = 'Pipeline_DOES_NOT_EXIST'

class PipelineBranchDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Pipeline branch does not exist.'
    error_code = 'Pipeline_BRANCH_DOES_NOT_EXIST'

class JsonNotValidError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'JSON is not valid. [{error}]'
    error_code = 'JSON_NOT_VALID'

class SchemaDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Schema does not exist.'
    error_code = 'SCHEMA_DOES_NOT_EXIST'
