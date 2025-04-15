from typing import Optional, List
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship
from app.models.base import TimestampModel
from app.core.config import Config
from pydantic import BaseModel 


class PublishDetailsBase(SQLModel):
    publish_id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.customer.customer_id")
    bh_project_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.bh_project.bh_project_id")
    delivery_name: str = Field(..., description="Delivery name")
    connection_id: int = Field(..., description="Connection ID")
    zone_cd: Optional[int] = Field(None, description="Zone code")
    source_setup_cd: Optional[int] = Field(None, description="Source setup code")
    delivery_option_cd: Optional[int] = Field(None, description="Delivery option code (Full, Incremental)")
    file_format_cd: Optional[int] = Field(None, description="File format code (CSV, Parquet, JSON)")
    delimiter_cd: Optional[int] = Field(None, description="Delimiter code (Comma, Tab)")
    compression: Optional[int] = Field(None, description="Compression type code")
    tag: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Tags")
    delivery_type_cd: Optional[int] = Field(None, description="Delivery type code (Event-driven, Scheduled, One-time delivery)")
    schedule_details: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Schedule details")
    alert_setting: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Alert settings")
    last_batch_id: Optional[int] = Field(None, description="Last successful batch ID delivered to customer")
    last_batch_on: Optional[str] = Field(None, description="Timestamp watermark for last successful batch")
    created_on: Optional[str] = Field(None, description="Created on timestamp")
    created_by: str = Field(..., description="Created by")
    updated_on: Optional[str] = Field(None, description="Updated on timestamp")
    updated_by: str = Field(None, description="Updated by")


class PublishDetails(PublishDetailsBase, TimestampModel, table=True):
    __tablename__ = "publish_details"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    customer: "Customer" = Relationship(back_populates="publish_details")
    bh_project: "BHProject" = Relationship(back_populates="publish_details")
    publish_queries: List["PublishQueryDetails"] = Relationship(back_populates="publish_details")


class PublishDetailsCreate(PublishDetailsBase):
    pass


class PublishDetailsUpdate(SQLModel):
    customer_id: Optional[int] = None
    bh_project_id: Optional[int] = None
    delivery_name: Optional[str] = None
    connection_id: Optional[int] = None
    zone_cd: Optional[int] = None
    source_setup_cd: Optional[int] = None
    delivery_option_cd: Optional[int] = None
    file_format_cd: Optional[int] = None
    delimiter_cd: Optional[int] = None
    compression: Optional[int] = None
    tag: Optional[dict] = None
    delivery_type_cd: Optional[int] = None
    schedule_details: Optional[dict] = None
    alert_setting: Optional[dict] = None
    last_batch_id: Optional[int] = None
    last_batch_on: Optional[str] = None
    created_on: Optional[str] = None
    created_by: Optional[str] = None
    updated_on: Optional[str] = None
    updated_by: Optional[str] = None


class PublishQueryDetailsBase(SQLModel):
    query_id: Optional[int] = Field(default=None, primary_key=True)
    query: str = Field(..., description="Query")
    display_name: Optional[str] = Field(..., description="Display Name")
    is_validated: bool = Field(..., description="If query is valid, it is set to true")
    publish_id: Optional[int] = Field(None, foreign_key=f"{Config.DB_SCHEMA}.publish_details.publish_id")
    is_save: bool = Field(default=False, description="If true, the query is saved")


class PublishQueryDetails(PublishQueryDetailsBase, TimestampModel, table=True):
    __tablename__ = "publish_query_details"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # customer_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.customer.customer_id")
    publish_details: "PublishDetails" = Relationship(back_populates="publish_queries")


class PublishQueryDetailsCreate(PublishQueryDetailsBase):
    pass


class PublishQueryDetailsUpdate(SQLModel):
    query: Optional[str] = None
    is_validated: Optional[bool] = None


class PublishDetailsReturn(PublishDetailsBase, TimestampModel):
    pass


class PublishQueryDetailsReturn(PublishQueryDetailsBase, TimestampModel):
    pass
