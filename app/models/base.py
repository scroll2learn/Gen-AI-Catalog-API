from sqlmodel import SQLModel, Field, Column, DateTime

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import text, Integer, ForeignKey, Column
from app.core.config import Config

from typing import Optional
from pydantic import EmailStr

class IDModel(SQLModel):
    id: int = Field(default=None, primary_key=True)

class UserDetailBase(SQLModel):
    user_detail_id: int = Field(default=None, primary_key=True)
    username: str = Field(..., min_length=1, max_length=100)
    user_email: EmailStr = Field(...)

class UserDetail(UserDetailBase, table=True):
    __tablename__ = "user_detail"
    __table_args__ = {"schema": Config.DB_SCHEMA}

class UserDetailReturn(SQLModel):
    user_detail_id: int = None
    username: str = None
    user_id: int = None

class TimestampModel(SQLModel):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
            ),
        )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"),
            onupdate=func.now()
            ),
        )
    
    created_by: Optional[int] = Field(
        None, 
        nullable=True,
        sa_column=Column(
            Integer, 
            ForeignKey(f"{Config.DB_SCHEMA}.user_detail.user_detail_id", ondelete="CASCADE")
        ),
        description="ID of the user who created the record"
    )
    
    updated_by: Optional[int] = Field(
        None, 
        nullable=True,
        sa_column=Column(
            Integer, 
            ForeignKey(f"{Config.DB_SCHEMA}.user_detail.user_detail_id", ondelete="CASCADE")
        ),
        description="ID of the user who last updated the record"
    )

    is_deleted: Optional[bool] = Field(
        default=False,
        nullable=True,
        description="Whether the pipeline is deleted"
    )

    deleted_by: Optional[int] = Field(
        None, 
        nullable=True,
        sa_column=Column(
            Integer, 
            ForeignKey(f"{Config.DB_SCHEMA}.user_detail.user_detail_id", ondelete="CASCADE")
        ),
        description="ID of the user who deleted the record"
    )

class StatusMessage(SQLModel):
    status: bool
    message: str
