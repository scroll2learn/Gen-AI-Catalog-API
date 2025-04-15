from typing import Optional, List, Union
from app.connections.destination.models.bigquery import DestinationBigquery
from app.connections.destination.models.connection_local import DestinationLocal
from app.connections.destination.models.gcs import DestinationGCS
from app.connections.destination.models.mysql import DestinationMySql
from app.connections.destination.models.oracle import DestinationOracle
from app.connections.destination.models.postgres import DestinationPostgres
from app.connections.destination.models.s3 import DestinationS3
from app.connections.destination.models.snowflake import DestinationSnowflake
from app.connections.source.models.bigquery import SourceBigQuery
from app.connections.source.models.connection_local import SourceLocal
from app.connections.source.models.gcs import SourceGCS
from app.connections.source.models.mysql import SourceMySql
from app.connections.source.models.oracle import SourceOracle
from app.connections.source.models.postgres import SourcePostgres
from app.connections.source.models.s3 import SourceS3
from app.connections.source.models.snowflake import SourceSnowflake
from app.enums.connection_registry import (
    ConnectionStatusEnum,
    ConnectionTypes,
    GeographyEnum,
    SourceType,
)
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship

from app.models.base import TimestampModel
from app.core.config import Config
from app.enums import ArgFieldTypes


# Connection Registri is for all differant types of connections to be registered
"""
Example JSON payload:
{
    "connection_name": "snowflake",
    "connection_description": "",
    "connection_policies_description": "",
    "connection_args": [
        {
            "arg_name": "User Name",
            "default_value": null,
            "field_type": "STRING",
            "optional": false,
            "description": "Provide username for target Snowflake database",
            "options": null
        },
        {
            "arg_name": "Password",
            "default_value": null,
            "field_type": "PASSWORD",
            "optional": false,
            "description": "Provide password for the given username",
            "options": null
        },
        {
            "arg_name": "Host Name",
            "default_value": null,
            "field_type": "STRING",
            "optional": false,
            "description": "Provide target Snowflake database name",
            "options": null
        },
        {
            "arg_name": "Port",
            "default_value": null,
            "field_type": "INTEGER",
            "optional": false,
            "description": "Provide port for target Snowflake database",
            "options": null
        },
        {
            "arg_name": "Public",
            "default_value": null,
            "field_type": "DROPDOWN",
            "optional": false,
            "description": "Will this connection be publicly available?",
            "options": ["Yes", "No"]
        }
    ]
}
"""

# connection Configs, i.e. individual values for each connection type, using a connection registry

"""
Example JSON payload:
{
    "connection_config_name": "snowflake-aws",
    "connection_id": 4,
    "connection_arg_values": {
        "User Name": "dbuser",  # encrypted
        "Password": "abc123",  # encrypted
        "Host Name": "bh.com",  # encrypted
        "Port": 22,  # encrypted
"""


class ConnectionArgs(SQLModel):
    arg_name: str
    arg_key: Optional[str]
    description: Optional[str]
    field_type: ArgFieldTypes
    default_value: Optional[str]
    Optional: Optional[bool]
    options: Optional[List[str]]
    oneof: Optional[list[dict]]

    class Config:
        use_enum_values = True


class ConnectionRegistryBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    connection_name: str = Field(..., min_length=1, description="Connection Type")
    connection_display_name: str = Field(
        default=None, nullable=True, min_length=1, description="Connection display name"
    )
    connection_description: str = Field(
        ..., min_length=1, description="Description about Connection Type"
    )
    connection_type: Optional[ConnectionTypes] = Field(
        default=ConnectionTypes.SOURCE, nullable=True, description="Connection Type"
    )


class ConnectionConfigBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    connection_config_name: str = Field(
        ..., min_length=1, description="Connection name assigned by user"
    )
    custom_metadata: dict = Field(
        nullable=False,
        sa_column=Column(JSON, nullable=False),
        description="Args Required",
    )
    connection_id: int = Field(
        foreign_key=f"{Config.DB_SCHEMA}.bh_connection_registry.id"
    )
    connection_name: str = Field(
        ...,
        min_length=1,
        description="Connection Name. Example: Snowflake, Bigquery, etc",
    )
    connection_type: ConnectionTypes = Field(
        default=ConnectionTypes.SOURCE,
        nullable=True,
        description="Connection Type. Example: Source, Destination",
    )
    connection_status: Optional[ConnectionStatusEnum] = Field(
        default=ConnectionStatusEnum.ACTIVE,
        nullable=True,
        description="Connection Status",
    )
    data_residency: Optional[GeographyEnum] = Field(
        default=GeographyEnum.AUTO, nullable=True, description="Data Residency"
    )
    secret_name: Optional[str] = Field(
        default=None, nullable=True, description="Secret Name"
    )


class ConnectionRegistry(ConnectionRegistryBase, TimestampModel, table=True):
    __tablename__ = "bh_connection_registry"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # Relationships with children
    bh_connection_config: Optional[List["ConnectionConfig"]] = Relationship(
        back_populates="bh_connection_registry",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class ConnectionConfig(ConnectionConfigBase, TimestampModel, table=True):
    __tablename__ = "bh_connection_config"
    __table_args__ = {"schema": Config.DB_SCHEMA}

    # Relationships with Parent
    bh_connection_registry: ConnectionRegistry = Relationship(
        back_populates="bh_connection_config"
    )

    # Relationships with children
    data_source: Optional[List["DataSource"]] = Relationship(
        back_populates="connection_config", sa_relationship_kwargs={"lazy": "selectin"}
    )


class ConnectionRegistryCreate(SQLModel):
    connection_name: str
    connection_display_name: Optional[str]
    connection_description: Optional[str]
    connection_type: Optional[ConnectionTypes]


class ConnectionRegistryUpdate(SQLModel):
    connection_id: Optional[int]
    connection_name: Optional[str]
    connection_display_name: Optional[str]
    connection_description: Optional[str]
    connection_type: Optional[ConnectionTypes]


ConfigUnion = Union[
    SourceSnowflake,
    SourceBigQuery,
    DestinationBigquery,
    DestinationSnowflake,
    SourceLocal,
    DestinationLocal,
    SourcePostgres,
    DestinationPostgres,
    DestinationMySql,
    DestinationOracle,
    SourceMySql,
    SourceOracle,
    SourceS3,
    DestinationS3,
    SourceGCS,
    DestinationGCS,
]


class ConnectionConfigCreate(SQLModel):
    connection_config_name: str
    custom_metadata: dict
    connection_id: int
    connection_name: str
    connection_type: ConnectionTypes
    connection_status: ConnectionStatusEnum
    data_residency: GeographyEnum
    secret_name: Optional[str]
    config: str  # Stored in secret Manager not in database
    init_vector: str  # Created freshly for every API Call
    config_union: Optional[ConfigUnion]


class ConnectionConfigUpdate(SQLModel):
    connection_name: Optional[str]
    connection_description: Optional[str]
    connection_type: Optional[ConnectionTypes]
    custom_metadata: Optional[dict]
    connection_status: Optional[ConnectionStatusEnum]
    data_residency: Optional[GeographyEnum]
    config: Optional[str]
    init_vector: Optional[str]


class ConnectionRegistryReturn(ConnectionRegistryBase):
    pass


class ConnectionConfigReturn(ConnectionConfigBase):
    config: Optional[str]
    connection_type: Optional[str]  # Derived from Connection Registry Connection Name
    init_vector: Optional[str]
