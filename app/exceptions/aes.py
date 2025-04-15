from fastapi import status
from app.exceptions import BaseHTTPException


class AESEncryptionError(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = (
        '{value} cannot be decrypted. Please note API expects a utf-8-encoded PKCS7-padded value '
        'AES-encrypted in CBC mode, using a 32-byte key and a 16-byte iv, in base64'
    )
    error_code = 'AES_ENCRYPTION_ERROR'
