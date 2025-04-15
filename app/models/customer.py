from typing import Optional, List
from app.enums.bh_project import Status
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship
from pydantic import BaseModel

from app.models.base import TimestampModel
from app.core.config import Config
from app.models.pulish_data import PublishDetails


class CustomerBase(SQLModel):
    customer_id: int = Field(default=None, primary_key=True)
    relation_ship_owner: str = Field(..., description="The relationship owner name")
    relation_ship_owner_email: str = Field(..., min_length=1, description="The relationship owner email")
    technology_owner: str = Field(..., min_length=1, description="The technology owner name")
    technology_owner_email: str = Field(..., min_length=1, description="The technology owner email")
    tags: dict = Field(default=None, nullable=True, sa_column=Column(JSON), description="Tags for linege")
    alert_setting: dict = Field(default=None, nullable=True, sa_column=Column(JSON), description="settings for alert")
    status: Status = Field(default=Status.ACTIVE, nullable=True, description="Status of project if its Active or Inactive")

class Customer(CustomerBase, TimestampModel, table=True):
    __tablename__ = "customer"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    connection_dtl: Optional[List["ConnectionDtl"]] = Relationship(back_populates="customer", sa_relationship_kwargs={"lazy": "selectin"})
    publish_details: List[PublishDetails] = Relationship(back_populates="customer", sa_relationship_kwargs={"lazy": "selectin"})

class CustomerCreate(SQLModel):
    relation_ship_owner: str = None
    relation_ship_owner_email: str = None
    technology_owner: str = None
    technology_owner_email: str = None
    tags: dict = None
    alert_setting: dict = None


class CustomerUpdate(SQLModel):
    relation_ship_owner: Optional[str] = None
    relation_ship_owner_email: Optional[str] = None
    technology_owner: Optional[str] = None
    technology_owner_email: Optional[str] = False
    tags: Optional[dict] = None
    alert_setting: Optional[dict] = None
    status_cd: Optional[int] = None
    

class ConnectionDtlBase(SQLModel):
    connection_dtl_id: int = Field(default=None, primary_key=True)
    connection_name: str = Field(..., description="connection name")
    target_delivery_platform_cd: int = Field(..., description="connection target delivery platfom cd")
    connection_details: dict = Field(default=None,nullable=True, sa_column=Column(JSON),description="connection details")
    # snow_flake_url: str = Field(default=0, nullable=False, description="snow flake url")
    # snow_flake_username: str = Field( nullable=True, description="snow flake user name")
    # snow_flake_password: str = Field( nullable=True, description="snow flake user password")
    # warehouse: str = Field(nullable=True, description="ware house")
    test_connection: bool = Field(nullable=False,default=False, description="ware house")

    # Foreign Keys 
    customer_id: int = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.customer.customer_id")


class ConnectionDtl(ConnectionDtlBase, TimestampModel, table=True):
    __tablename__ = "connection_dtl"
    __table_args__ = {'schema': Config.DB_SCHEMA}
    
    customer: Customer = Relationship(back_populates="connection_dtl")


class ConnectionDtlCreate(ConnectionDtlBase):
    pass


class ConnectionDtlUpdate(SQLModel):
    connection_name: Optional[str] = None
    target_delivery_platform_cd: Optional[int] = None
    connection_details: Optional[dict] = None
    # snow_flake_url: Optional[str] = None
    # snow_flake_username: Optional[str] = None
    # snow_flake_password: Optional[str] = None
    # warehouse: Optional[str] = None
    test_connection:Optional[bool]=None



class ConnectionDtlReturn(ConnectionDtlBase, TimestampModel):
    pass



class CustomerReturn(CustomerBase, TimestampModel):
    connection_dtl: Optional[List[ConnectionDtl]] = []
    total_extracts_config: int = 0
