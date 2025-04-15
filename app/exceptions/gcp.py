from fastapi import status
from app.exceptions import BaseHTTPException


class BHGCPClientError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = (
        'Client for service {service} in project {project_nbr} failed, error code: {error_code}'
    )
    error_code = 'GCP_CLIENT_ERROR'

class BHSecretCreateError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = (
        'Creation of service for [{name}] failed, error: {error}'
    )
    error_code = 'SECRET_CREATE_ERROR'
