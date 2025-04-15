from fastapi import status
from app.exceptions import BaseHTTPException


class DSMissingRequiredParameter(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'At least one of `data_source_name`, or `data_source_key` must be provided.'
    error_code = 'MISSING_REQUIRED_PARAMETER'

class DataSourceAlreadyExists(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    message = ('Data source already exists with name [{name}]. '
               'Delete the existing data source or provide a '
               'different name for the new data source.')
    error_code = 'DATA_SOURCE_ALREADY_EXISTS'
