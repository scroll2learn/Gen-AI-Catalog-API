from typing import List, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str

class QueryResult(BaseModel):
    columns: List[str]
    rows: List[List[str]]

class AWSCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    location: str = "us-east-1"
    init_vector: str

class BucketModel(BaseModel):
    name: str

class ConnectionTestResponse(BaseModel):
    status: str
    buckets: List[BucketModel]

class SnowflakeCredentials(BaseModel):
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    db_schema: str = Field(alias='schema')  # Use alias for 'schema'

class GCSCredentials(BaseModel):
    project_id: str
    client_email: str
    private_key: str
    
class BigQueryCredentials(BaseModel):
    project_id: str
    client_email: str
    private_key: str
    
class DatabricksCredentials(BaseModel):
    server_hostname: str
    http_path: str
    access_token: str
