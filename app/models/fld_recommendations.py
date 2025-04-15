from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config


class FieldRecommendationsBase(SQLModel):
    rule_id: int = Field(default=None, primary_key=True)
    rule_name: str = Field(..., min_length=1, max_length=64, description="The name of the Rule")
    rule_dq_type_id: int = Field(..., description="Data Quality Type")
    rule_params: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True), description="Data Quality Parameters")
    rule_dq_level: Optional[str] = Field(default='ERROR', description="Data Quality Level")
    rule_fld_id: Optional[int] = None
    rule_status: Optional[str] = None
    rule_rejected_by: Optional[str] = None
    rule_accepted_by: Optional[str] = None
    rule_lyt_id: Optional[int] = None


class FieldRecommendations(FieldRecommendationsBase, TimestampModel, table=True):
    __tablename__ = "fld_recommendations"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class FieldRecommendationsCreate(FieldRecommendationsBase):
    pass


class FieldRecommendationsUpdate(SQLModel):
    rule_status: Optional[str] = None
    rule_rejected_by: Optional[str] = None
    rule_accepted_by: Optional[str] = None


class FieldRecommendationsReturn(FieldRecommendationsBase, TimestampModel):
    pass
