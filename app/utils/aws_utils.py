from random import choices
from string import ascii_lowercase, digits
from app.services.aes import encrypt_string


def get_aws_encrypted_keys(aws_secret: dict):
    # Encrypt secret values 
    access_key = aws_secret.get('aws_access_key')
    secret_access_key = aws_secret.get('aws_secret_access_key')
    access_key, init_vector = encrypt_string(access_key)
    secret_access_key, init_vector = encrypt_string(secret_access_key)
    return access_key, secret_access_key
