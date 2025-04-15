from typing import Optional, Union
from pydantic import BaseModel, Field
from enum import Enum



class SourceSnowflakeSchemasCredentialsAuthType(str, Enum):
    USERNAME_PASSWORD = 'username/password'
    OAUTH = 'OAuth'
    

class SourceSnowflakeUsernameAndPassword(BaseModel):
    username: str
    password: str
    auth_type: SourceSnowflakeSchemasCredentialsAuthType = SourceSnowflakeSchemasCredentialsAuthType.USERNAME_PASSWORD

class SourceSnowflakeOAuth20(BaseModel):
    client_id: str
    client_secret: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    auth_type: SourceSnowflakeSchemasCredentialsAuthType = SourceSnowflakeSchemasCredentialsAuthType.OAUTH


SourceSnowflakeAuthorizationMethod = Union[SourceSnowflakeUsernameAndPassword, SourceSnowflakeOAuth20]

class SourceSnowflake(BaseModel):
    host: str
    role: str
    warehouse: str
    database: str
    schema_: Optional[str] = Field(None, alias="schema")
    jdbc_url_params: Optional[str]
    credentials: Optional[SourceSnowflakeAuthorizationMethod]
    source_type: str = "snowflake"

    def dict_with_serialized_enum(self):
        """Returns a dict with the Enum fields serialized as strings."""
        data = self.dict()
        if isinstance(self.credentials, BaseModel):
            credentials_data = self.credentials.dict()
            if isinstance(self.credentials.auth_type, Enum):
                credentials_data['auth_type'] = self.credentials.auth_type.value
            data['credentials'] = credentials_data
        return data