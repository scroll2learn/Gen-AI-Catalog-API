from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    id: UUID = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = 'API Error'
    error_code: str = 'API_ERROR'
    context: Optional[Dict[str, Any]] = {}
    headers: Optional[Dict[str, Any]] = None

    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.id = uuid4()
        if context:
            self.context = context
        super().__init__(self.status_code, detail=self.message, headers=self.headers)
    
    @property
    def formatted_message(self) -> Dict[str, Any]:
        if not self.context:
            return self.message
        return self.message.format(**self.context)
    
    @property
    def api_response(self):
        return {
            'error_id': str(self.id),
            'error_code': self.error_code,
            'message': self.formatted_message,
            'error_code': self.error_code,
        }
    
    def __str__(self):
        return f'{self.error_code}: {self.formatted_message}'


class ObjectNotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Object not found for {column_name!r}: {id!r} and type: {type!r}'
    error_code = 'OBJECT_NOT_FOUND'


class APIException(BaseHTTPException):
    status_code = '{status_code}'
    message = '{message}'
    error_code = '{API_ERROR}'


class CreateException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST 
    message = 'Creation failed: {error}'
    error_code = 'CREATE_ERROR'
