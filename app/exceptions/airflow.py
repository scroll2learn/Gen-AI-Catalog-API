from fastapi import status
from app.exceptions import BaseHTTPException

class AirflowException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Airflow Error: {message}'
    error_code = 'AIRFLOW_ERROR'