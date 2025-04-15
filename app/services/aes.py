import os
from base64 import b64decode, b64encode
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fastapi import HTTPException, status

# Remove these imports since we're defining them here
# from app.exceptions import AESEncryptionError
# from app.core.config import Config

# Define your AESEncryptionError exception if not already defined
class AESEncryptionError(Exception):
    def __init__(self, message, context):
        super().__init__(message)
        self.context = context

# Configuration placeholder
class Config:
    DECRYPTION_KEY = 'passwordpasswordpasswordpassword'  # Replace with your actual key

def encrypt_string(string: str, init_vector: str = None) -> Tuple[str, str]:

    # Generate random IV if not provided and encode it as Base64
    if not init_vector:
        init_vector_bytes = os.urandom(16)
        init_vector = b64encode(init_vector_bytes).decode('utf-8')
    else:
        # Decode the provided IV from Base64
        init_vector_bytes = b64decode(init_vector)

    decryption_key = Config.DECRYPTION_KEY.encode('utf-8')  # Should be 16, 24, or 32 bytes

    aes = AESEncryptorService(decryption_key, init_vector_bytes)
    encrypted_bytes = aes.encrypt(string)

    # Encode the encrypted bytes as a Base64 string
    encrypted_string_b64 = b64encode(encrypted_bytes).decode('utf-8')

    return encrypted_string_b64, init_vector

def decrypt_string(encrypted_string: str, init_vector: str, ignore_encryption: bool = False) -> str:
    try:
        decryption_key = Config.DECRYPTION_KEY.encode('utf-8')  # Should be 16, 24, or 32 bytes

        # Decode the IV from Base64
        iv = b64decode(init_vector)

        aes = AESEncryptorService(decryption_key, iv)

        # Decode the encrypted string from Base64
        encrypted_bytes = b64decode(encrypted_string)

        decrypted_string = aes.decrypt(encrypted_bytes)
        return decrypted_string
    except AESEncryptionError as e:
        if ignore_encryption:
            print('Decryption failed, string may not be encrypted, storing as-is')
            return encrypted_string
        # If you want to return this exception message to the user, raise HTTPException here
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Decryption error: {str(e)}"
        )

class AESEncryptorService:
    def __init__(self, key: bytes, iv: bytes, encoding: str = 'utf-8') -> None:
        key_length = len(key)
        if key_length not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes long")
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes long")

        self.key = key
        self.iv = iv
        self.encoding = encoding

    def encrypt(self, plain_text: str) -> bytes:
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        byte_text = plain_text.encode(self.encoding)
        padded_text = pad(byte_text, AES.block_size)
        cipher_text = aes.encrypt(padded_text)
        return cipher_text

    def decrypt(self, cipher_text: bytes) -> str:
        try:
            aes = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted_padded = aes.decrypt(cipher_text)
            decrypted = unpad(decrypted_padded, AES.block_size)
            plain_text = decrypted.decode(self.encoding)
            return plain_text
        except Exception as e:
            raise AESEncryptionError("Decryption failed", context={'value': 'Password'}) from e