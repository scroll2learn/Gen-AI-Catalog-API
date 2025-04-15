from fastapi import status
from app.exceptions import BaseHTTPException


class InvalidRegexProvided(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Invalid regex provided.'
    error_code = 'INVALID_REGEX_PROVIDED'
