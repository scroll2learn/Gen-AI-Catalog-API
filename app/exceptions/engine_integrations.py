
from fastapi import status
from app.exceptions import BaseHTTPException


class MissingRequiredParameter(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'At least one of `data_source_id`, `data_source_name`, or `data_source_key` must be provided.'
    error_code = 'MISSING_REQUIRED_PARAMETER'
