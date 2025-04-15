from typing import Optional
from pydantic import BaseModel

class DestinationS3(BaseModel):
    bucket_name: Optional[str] = None
    access_key: str
    secret_key: str
    region: Optional[str] = None
    role_arn: Optional[str] = None
    destination_type: str = "s3"
