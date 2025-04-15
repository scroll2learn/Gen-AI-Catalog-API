from typing import Optional
from pydantic import BaseModel

class DestinationOracle(BaseModel):
    host: str
    port: int
    service_name: Optional[str]  # Oracle uses service_name or SID
    sid: Optional[str]  # Some setups may require SID instead of service_name
    username: str
    password: str
    db_schema: Optional[str]  # Schema within Oracle DB
    destination_type: str = "oracle"
