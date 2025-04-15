import json
import logging
import os
from typing import List, Optional
from urllib.parse import parse_qs

from app.exceptions.gcp import BHSecretCreateError
from app.services.aes import decrypt_string
from app.utils.cloud_service_utils import get_secret_manager_formatted_name
from app.utils.constants import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app.api.deps import get_context
from app.core.context import Context
from app.models.aws import (AWSCredentials, BigQueryCredentials,
                            ConnectionTestResponse, DatabricksCredentials,
                            GCSCredentials, QueryRequest, QueryResult,
                            SnowflakeCredentials)
from app.models.base import StatusMessage
from app.services.aws import AWSMWAAService, AthenaQueryService
from app.utils.auth_wrapper import authorize

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Get environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")
database = os.getenv("DATABASE")
output_bucket = os.getenv("OUTPUT_BUCKET")

# # Initialize Athena service
# athena_service = AthenaQueryService(
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     region_name=region_name,
#     database=database,
#     output_bucket=output_bucket,
# )


# @router.post(
#     "/athena_query", response_model=QueryResult, status_code=http_status.HTTP_200_OK
# )
# async def athena_query(
#     request: QueryRequest,
#     ctx: Context = Depends(get_context),
#     authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
# ):
#     try:
#         query_execution_id = athena_service.run_athena_query(request.query)
#         results = athena_service.get_query_results(query_execution_id)
#         return results
#     except Exception as e:
#         logger.error(f"Error executing Athena query: {e}")
#         raise HTTPException(
#             status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
#         )


@router.post(
    "/test_connection",
    status_code=http_status.HTTP_200_OK,
)
async def test_aws_connections(
    credentials: AWSCredentials,
    bh_env_name: str,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    try:
        # Decrypt AWS credentials
        credentials.aws_access_key_id = decrypt_string(credentials.aws_access_key_id, credentials.init_vector)
        credentials.aws_secret_access_key = decrypt_string(credentials.aws_secret_access_key, credentials.init_vector)
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to decrypt AWS credentials: {e}"
        )
    try:
        await ctx.test_connection_service.test_aws_connection(
            credentials=credentials
        )
    except Exception as e:
        logger.error(f"Error testing AWS connection: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    try:
        secret_name = get_secret_manager_formatted_name(bh_env_name)
        # Storing access and secret access key on secret manager AWS
        secret_data = json.dumps(
            {AWS_ACCESS_KEY: credentials.aws_access_key_id, AWS_SECRET_ACCESS_KEY: credentials.aws_secret_access_key}
        )
        secret, version = await ctx.aws_service.secrets.new_secret(
            secret_name, secret_data
        )
        return {
            "success": "true",
            "pvt_key": version,
        }

    except Exception as e:
        raise BHSecretCreateError(context={"error": str(e), "name": bh_env_name})


@router.post(
    "/test_snowflake_connection",
    response_model=ConnectionTestResponse,
    status_code=http_status.HTTP_200_OK,
)
async def test_snowflake_connection(
    credentials: SnowflakeCredentials,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    try:
        return await ctx.test_snowflake_connection_service.test_snowflake_connection(
            credentials=credentials
        )
    except Exception as e:
        logger.error(f"Error testing Snowflake connection: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/test_gcs_connection",
    response_model=ConnectionTestResponse,
    status_code=http_status.HTTP_200_OK,
)
async def test_gcs_connection(
    *,
    credentials: GCSCredentials,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    print("##########################")
    print(credentials)
    return await ctx.test_gcs_connection_service.test_gcs_connection(
        credentials=credentials
    )


@router.post(
    "/test_bigquery_connection",
    response_model=ConnectionTestResponse,
    status_code=http_status.HTTP_200_OK,
)
async def test_bigquery_connection(
    *,
    credentials: BigQueryCredentials,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    print("##########################")
    print(credentials)
    return await ctx.test_bigquery_connection_service.test_bigquery_connection(
        credentials=credentials
    )


@router.post(
    "/test_databricks_connection",
    response_model=ConnectionTestResponse,
    status_code=http_status.HTTP_200_OK,
)
async def test_databricks_connection(
    *,
    credentials: DatabricksCredentials,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
):
    print("##########################")
    print(credentials)
    return await ctx.test_databricks_connection_service.test_databricks_connection(
        credentials=credentials
    )
