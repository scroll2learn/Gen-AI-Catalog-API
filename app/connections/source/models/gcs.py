from pydantic import BaseModel

class SourceGCS(BaseModel):
    bucket_name: str
    credentials_json: dict
    source_type: str = "gcs"