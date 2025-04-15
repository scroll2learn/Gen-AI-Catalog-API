from fastapi import status
from app.exceptions import BaseHTTPException


class NotValidConnectionType(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Not a valid connection type'
    error_code = 'NOT_VALID_CONNECTION_TYPE'