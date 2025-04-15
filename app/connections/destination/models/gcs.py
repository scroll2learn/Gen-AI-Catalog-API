from pydantic import BaseModel

class DestinationGCS(BaseModel):
    bucket_name: str
    credentials_json: dict
    destination_type: str = "gcs"
