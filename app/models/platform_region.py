from sqlmodel import SQLModel, Field
from typing import List, Optional
from app.models.codes_hdr import CodesDtl

from app.core.config import Config


class PlatformRegionBase(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)
    description: str = Field(default=None, nullable=False)
    region_identifier: str = Field(default=None, nullable=False, unique=True)
    platform_cd: int = Field(default=None, nullable=False, foreign_key=f"{Config.DB_SCHEMA}.codes_dtl.id")


class PlatformRegion(PlatformRegionBase, table=True):
    __tablename__ = "platform_region"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class PlatformRegionCreate(PlatformRegionBase): 
    pass


class PlatformRegionUpdate(PlatformRegionBase): 
    pass


class PlatformRegionReturn(PlatformRegionBase):
    codes_dtl: Optional[CodesDtl] = {}
