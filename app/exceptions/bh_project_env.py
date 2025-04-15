from fastapi import status
from app.exceptions import BaseHTTPException

class BHGCPJsonFileError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = (
        'File must be a JSON.'
    )
    error_code = 'GCP_JSON_FILE_ERROR'

class BHProjectEnvDataInvalidError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = (
        '{error}'
    )
    error_code = 'PROJECT_ENV_DATA_INVALID_ERROR'