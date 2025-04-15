from typing import Optional, List
from app.models.flow import Flow,FlowReturn
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship, Field

from app.models.base import TimestampModel
from app.core.config import Config
from app.models.bh_project import ProjectEnvironment
# from app.models.flow import Flow, FlowDeployment

class BHReleaseBundleBase(SQLModel):
    bh_bundle_id: int = Field(default=None, primary_key=True)
    bh_bundle_name: str = Field(..., min_length=1, description="The name of the release bundle")
    bh_bundle_description: str = Field(..., description="Description about the release")

class BHReleaseBundle(BHReleaseBundleBase, TimestampModel, table=True):
    __tablename__ = "bh_bundle"
    __table_args__ = {'schema': Config.DB_SCHEMA}
    flow: Optional[List["Flow"]] = Relationship(
        back_populates="bh_bundle", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class BHReleaseBundleCreate(BHReleaseBundleBase):
    bh_bundle_name: str
    bh_bundle_description: str
    flow: Optional[List[int]]


class BHReleaseBundleUpdate(TimestampModel):
    bh_bundle_name: str
    bh_bundle_description: str

class BHReleaseBundleReturn(BHReleaseBundleBase, TimestampModel):
   flow: Optional[List[FlowReturn]] = []
    