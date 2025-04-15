from typing import Optional
from pydantic import BaseModel

class SourceBigQuery(BaseModel):
    project_id: str
    dataset_id: Optional[str]
    credentials_json: dict
    source_type: str = "bigquery"