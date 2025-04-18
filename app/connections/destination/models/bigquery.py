from typing import Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class DatasetLocation(str, Enum):
    US = 'US'
    EU = 'EU'
    ASIA_EAST1 = 'asia-east1'
    ASIA_EAST2 = 'asia-east2'
    ASIA_NORTHEAST1 = 'asia-northeast1'
    ASIA_NORTHEAST2 = 'asia-northeast2'
    ASIA_NORTHEAST3 = 'asia-northeast3'
    ASIA_SOUTH1 = 'asia-south1'
    ASIA_SOUTH2 = 'asia-south2'
    ASIA_SOUTHEAST1 = 'asia-southeast1'
    ASIA_SOUTHEAST2 = 'asia-southeast2'
    AUSTRALIA_SOUTHEAST1 = 'australia-southeast1'
    AUSTRALIA_SOUTHEAST2 = 'australia-southeast2'
    EUROPE_CENTRAL1 = 'europe-central1'
    EUROPE_CENTRAL2 = 'europe-central2'
    EUROPE_NORTH1 = 'europe-north1'
    EUROPE_SOUTHWEST1 = 'europe-southwest1'
    EUROPE_WEST1 = 'europe-west1'
    EUROPE_WEST2 = 'europe-west2'
    EUROPE_WEST3 = 'europe-west3'
    EUROPE_WEST4 = 'europe-west4'
    EUROPE_WEST6 = 'europe-west6'
    EUROPE_WEST7 = 'europe-west7'
    EUROPE_WEST8 = 'europe-west8'
    EUROPE_WEST9 = 'europe-west9'
    EUROPE_WEST12 = 'europe-west12'
    ME_CENTRAL1 = 'me-central1'
    ME_CENTRAL2 = 'me-central2'
    ME_WEST1 = 'me-west1'
    NORTHAMERICA_NORTHEAST1 = 'northamerica-northeast1'
    NORTHAMERICA_NORTHEAST2 = 'northamerica-northeast2'
    SOUTHAMERICA_EAST1 = 'southamerica-east1'
    SOUTHAMERICA_WEST1 = 'southamerica-west1'
    US_CENTRAL1 = 'us-central1'
    US_EAST1 = 'us-east1'
    US_EAST2 = 'us-east2'
    US_EAST3 = 'us-east3'
    US_EAST4 = 'us-east4'
    US_EAST5 = 'us-east5'
    US_SOUTH1 = 'us-south1'
    US_WEST1 = 'us-west1'
    US_WEST2 = 'us-west2'
    US_WEST3 = 'us-west3'
    US_WEST4 = 'us-west4'


class Bigquery(str, Enum):
    BIGQUERY = 'bigquery'


class DestinationBigqueryMethod(str, Enum):
    STANDARD = 'Standard'


class DestinationBigqueryCredentialType(str, Enum):
    HMAC_KEY = 'HMAC_KEY'


class GCSTmpFilesAfterwardProcessing(str, Enum):
    DELETE_ALL_TMP_FILES_FROM_GCS = 'Delete all tmp files from GCS'
    KEEP_ALL_TMP_FILES_IN_GCS = 'Keep all tmp files in GCS'


class Method(str, Enum):
    GCS_STAGING = 'GCS Staging'


class TransformationQueryRunType(str, Enum):
    INTERACTIVE = 'interactive'
    BATCH = 'batch'


class DestinationBigqueryHMACKey(BaseModel):
    hmac_key_access_id: str
    hmac_key_secret: str
    credential_type: DestinationBigqueryCredentialType = Field(DestinationBigqueryCredentialType.HMAC_KEY, alias="CREDENTIAL_TYPE")


class StandardInserts(BaseModel):
    method: DestinationBigqueryMethod = Field(DestinationBigqueryMethod.STANDARD, alias="METHOD")


class GCSStaging(BaseModel):
    credential: DestinationBigqueryHMACKey
    gcs_bucket_name: str
    gcs_bucket_path: str
    keep_files_in_gcs_bucket: Optional[GCSTmpFilesAfterwardProcessing] = Field(GCSTmpFilesAfterwardProcessing.DELETE_ALL_TMP_FILES_FROM_GCS, alias="keep_files_in_gcs_bucket")
    method: Method = Field(Method.GCS_STAGING, alias="METHOD")


class DestinationBigquery(BaseModel):
    dataset_id: str
    dataset_location: DatasetLocation
    project_id: str
    big_query_client_buffer_size_mb: Optional[int] = Field(15)
    credentials_json: Optional[dict] = None
    destination_type: Bigquery = Field(Bigquery.BIGQUERY, alias="DESTINATION_TYPE")
    disable_type_dedupe: Optional[bool] = Field(False)
    loading_method: Optional[Union[GCSStaging, StandardInserts]] = None
    raw_data_dataset: Optional[str] = None
    transformation_priority: Optional[TransformationQueryRunType] = Field(TransformationQueryRunType.INTERACTIVE)
    destination_type: str = "bigquery"
