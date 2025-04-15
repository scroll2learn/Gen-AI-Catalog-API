from typing import Optional
from pydantic import BaseModel

class DestinationPostgres(BaseModel):
    host: str
    port: int
    database: Optional[str]
    username: str
    password: str
    db_schema: Optional[str]
    destination_type: str = "postgres"
