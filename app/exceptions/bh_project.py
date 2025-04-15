from fastapi import status
from app.exceptions import BaseHTTPException


class BHProjectAlreadyExists(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'BH Project already exists with name [{name}]. Delete the existing BH Project or provide a different name for the new BH Project.'
    error_code = 'PROJECT_ALREADY_EXISTS'

class BHProjectDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'BH Project does not exist.'
    error_code = 'PROJECT_DOES_NOT_EXIST'

class DecryptExceptionError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Decryption failed: {error}'
    error_code = 'DECRYPT_EXCEPTION'

