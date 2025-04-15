
from fastapi import Depends
from app.exceptions.bh_project_env import BHGCPJsonFileError

from app.api.deps import get_context
from app.core.context import Context

def get_secret_manager_formatted_name(bh_env_name):
    formatted_bh_env_name = bh_env_name.replace(" ", "_").lower()
    secret_name = f"project_{formatted_bh_env_name}_secrets"
    return secret_name

def check_json_file_type(file):
    if file.content_type != "application/json":
        raise BHGCPJsonFileError()

async def get_cloud_decrypted_secrets(
    bh_env_name: str,
    cloud_type: str = "aws",
    ctx: Context = None
):
    if cloud_type == "aws":
        secret_name = get_secret_manager_formatted_name(bh_env_name)
        aws_secret = await ctx.aws_service.secrets.get_secret(secret_name)
        access_key = aws_secret.get('aws_access_key')
        secret_access_key = aws_secret.get('aws_secret_access_key')
        return access_key, secret_access_key
    elif cloud_type == "gcp":
        raise NotImplementedError("GCP not implemented")
    else:  
        raise ValueError("Invalid cloud type")
