from fastapi import status
from app.exceptions import BaseHTTPException

class FlowAlreadyExists(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Flow already exists with name [{name}].'
    error_code = 'FLOW_ALREADY_EXISTS'



class FlowNameMinimumLength(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Flow name must be at least 3 characters long.'
    error_code = 'FLOW_NAME_MINIMUM_LENGTH'



class FlowNameAlphanumeric(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Flow name must contain only alphanumeric characters.'
    error_code = 'FLOW_NAME_ALPHANUMERIC'

class FlowDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Flow does not exist.'
    error_code = 'FLOW_DOES_NOT_EXIST'

class FlowBranchDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Flow branch does not exist.'
    error_code = 'FLOW_BRANCH_DOES_NOT_EXIST'

class JsonNotValidError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'JSON is not valid. [{error}]'
    error_code = 'JSON_NOT_VALID'

class SchemaDoesNotExist(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Schema does not exist.'
    error_code = 'SCHEMA_DOES_NOT_EXIST'
