from pydantic import BaseModel

class SourceLocal(BaseModel):
    file_path_prefix: str
    source_type: str = "local"