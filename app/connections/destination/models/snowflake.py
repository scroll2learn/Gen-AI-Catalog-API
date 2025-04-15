from __future__ import annotations
from enum import Enum
from typing import Union, Optional
from pydantic import BaseModel, Field


class DestinationSnowflakeSchemasAuthType(str, Enum):
    O_AUTH2_0 = 'OAuth2.0'


class DestinationSnowflakeOAuth20(BaseModel):
    access_token: str = Field(..., description="Enter your application's Access Token")
    refresh_token: str = Field(..., description="Enter your application's Refresh Token")
    AUTH_TYPE: DestinationSnowflakeSchemasAuthType = Field(
        default=DestinationSnowflakeSchemasAuthType.O_AUTH2_0, alias="auth_type"
    )
    client_id: Optional[str] = Field(None, description="Enter your application's Client ID", alias="client_id")
    client_secret: Optional[str] = Field(None, description="Enter your application's Client Secret", alias="client_secret")

    class Config:
        allow_population_by_field_name = True


class DestinationSnowflakeAuthType(str, Enum):
    USERNAME_AND_PASSWORD = 'Username and Password'


class UsernameAndPassword(BaseModel):
    password: str = Field(..., description="Enter the password associated with the username.")
    AUTH_TYPE: DestinationSnowflakeAuthType = Field(
        default=DestinationSnowflakeAuthType.USERNAME_AND_PASSWORD, alias="auth_type"
    )

    class Config:
        allow_population_by_field_name = True


class DestinationSnowflakeSchemasCredentialsAuthType(str, Enum):
    KEY_PAIR_AUTHENTICATION = 'Key Pair Authentication'


class KeyPairAuthentication(BaseModel):
    private_key: str = Field(..., description="RSA Private key to use for Snowflake connection.")
    AUTH_TYPE: DestinationSnowflakeSchemasCredentialsAuthType = Field(
        default=DestinationSnowflakeSchemasCredentialsAuthType.KEY_PAIR_AUTHENTICATION, alias="auth_type"
    )
    private_key_password: Optional[str] = Field(
        None, description="Passphrase for private key", alias="private_key_password"
    )

    class Config:
        allow_population_by_field_name = True


class DestinationSnowflakeSnowflake(str, Enum):
    SNOWFLAKE = 'snowflake'

AuthorizationMethod = Union[KeyPairAuthentication, UsernameAndPassword, DestinationSnowflakeOAuth20]


class DestinationSnowflake(BaseModel):
    database: str = Field(..., description="Enter the name of the database you want to sync data into.")
    host: str = Field(..., description="Enter your Snowflake account's locator.")
    role: str = Field(..., description="Enter the role that you want to use to access Snowflake.")
    schema_: str = Field(..., alias="schema", description="Enter the name of the default schema.")
    username: str = Field(..., description="Enter the name of the user you want to use to access the database.")
    warehouse: str = Field(..., description="Enter the name of the warehouse.")
    credentials: Optional[AuthorizationMethod] = Field(None, description="Authorization method.")
    DESTINATION_TYPE: DestinationSnowflakeSnowflake = Field(
        default=DestinationSnowflakeSnowflake.SNOWFLAKE, alias="destinationType"
    )
    disable_type_dedupe: Optional[bool] = Field(
        False,
        description="Disable Writing Final Tables. WARNING! The data format in BH_data is likely stable but there are no guarantees that other metadata columns will remain the same in future versions.",
        alias="disable_type_dedupe",
    )
    jdbc_url_params: Optional[str] = Field(
        None, description="Enter the additional properties to pass to the JDBC URL.", alias="jdbc_url_params"
    )
    raw_data_schema: Optional[str] = Field(None, description="The schema to write raw tables into.", alias="raw_data_schema")
    retention_period_days: Optional[int] = Field(
        1, description="The number of days of Snowflake Time Travel to enable on the tables.", alias="retention_period_days"
    )
    destination_type: str = "snowflake"

    class Config:
        allow_population_by_field_name = True


