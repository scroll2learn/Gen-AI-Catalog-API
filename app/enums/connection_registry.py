from enum import Enum, auto


class ArgFieldTypes(Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    PASSWORD = "PASSWORD"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    FLOAT = "FLOAT"
    ARRAY = "ARRAY"
    JSON = "JSON"
    DROPDOWN = "DROPDOWN"
    MULTISELECT_DROPDOWN = "MULTISELECT_DROPDOWN"
    RADIO = "RADIO"

class ConnectionTypes(str, Enum):
    SOURCE = 'source'
    DESTINATION = 'destination'

class SourceType(str, Enum):
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    LOCAL = "local"
    POSTGRES = "postgres"
    S3 = "s3"
    MYSQL = "mysql"
    ORACLE = "oracle"
    GCS = "gcs"

class ConnectionStatusEnum(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DEPRECATED = 'deprecated'

class GeographyEnum(str, Enum):
    AUTO = 'auto'
    US = 'us'
    EU = 'eu'
