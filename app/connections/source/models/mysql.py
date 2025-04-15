from typing import Optional
from pydantic import BaseModel

class SourceMySql(BaseModel):
    host: str
    port: int
    database: Optional[str]
    username: str
    password: str
    db_schema: Optional[str]
    source_type: str = "mysql"
