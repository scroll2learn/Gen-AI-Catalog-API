from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, DateTime

from app.core.config import Config

from datetime import datetime
from sqlalchemy.sql import func


class AuditEventsBase(SQLModel):
    audit_id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(..., description="Event Type")
    bh_timestamp: datetime = Field(default_factory=func.now, sa_column=Column(DateTime(timezone=True)), nullable=False)
    object_id: Optional[int] = Field(default=None)
    object_type: Optional[str] = Field(default=None) # FIELD_VALIDATION # FIELD
    user_id: Optional[int] = Field(default=None)
    old_object: dict = Field(default=None, sa_column=Column(JSON, nullable=True), description="Old Object")
    new_object: dict = Field(default=None, sa_column=Column(JSON, nullable=True), description="New Object")
    comment: Optional[str] = Field(default=None, description="Comment")


class AuditEvents(AuditEventsBase, table=True):
    __tablename__ = "audit_events"
    __table_args__ = {'schema': Config.DB_SCHEMA, 'info': {'skip_autogenerate': True}}


class AuditEventsCreate(AuditEventsBase):
    pass


class AuditEventsReturn(AuditEventsBase):
    pass
