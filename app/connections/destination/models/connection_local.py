from typing import Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

class DestinationLocal(BaseModel):
    file_path_prefix: str
    destination_type: str = "local"
