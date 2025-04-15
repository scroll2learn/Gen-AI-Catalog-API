from typing import Optional, List, Union
from pydantic import Json
from sqlmodel import SQLModel

from app.models.data_source import (
    DataSourceReturn,
)
from app.models.data_source_layout import (
    DataSourceLayoutReturn,
)
from app.models.layout_fields import (
    LayoutFieldsReturn,
)


class ResponseModel(SQLModel):
    data_source: Optional[DataSourceReturn] = None
    data_source_layout: Optional[DataSourceLayoutReturn] = None
    layout_fields: Optional[List[LayoutFieldsReturn]] = []
    sample_data: Optional[Union[Json, List[Union[Json, dict]]]] = []


class FileProcessRequest(SQLModel):
    name: str = "Test Source 1"
    source_file_path: str = "s3a://bighammer-sample-data-development/01_DBC.csv"
    lake_zone_id: int = 1               #  Defaulted to Bronze Zone
    data_src_status_cd: int = 703       #  Defaulted to Draft
