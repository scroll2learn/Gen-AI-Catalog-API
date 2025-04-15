from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.models.base import TimestampModel
from app.core.config import Config


class JoinsBase(SQLModel):
    join_id: int = Field(default=None, primary_key=True)
    join_type_cd: int = Field(default=None, description="Represents Join Types")
    join_index: int = Field(..., description="Represents the order of the join")
    join_name: str = Field(..., description="Represents the alias name of the join")
    join_key: Optional[str] = Field(default=None, nullable=True, description="Represents the key of the join")
    join_desc: Optional[str] = Field(default=None, nullable=True, description="Represents the description of the join")
    left_data_src_lyt_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source_layout.data_src_lyt_id", description="Represents the left data source layout id")
    right_data_src_lyt_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source_layout.data_src_lyt_id", description="Represents the right data source layout id")
    left_data_src_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id", description="Represents the left data source id")
    right_data_src_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.data_source.data_src_id", description="Represents the right data source id")


class Joins(JoinsBase, TimestampModel, table=True):
    __tablename__ = "joins"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with children
    join_on: Optional[List["JoinOn"]] = Relationship(back_populates="joins", sa_relationship_kwargs={"lazy": "selectin"})

class JoinsCreate(JoinsBase):
    pass


class JoinsUpdate(SQLModel):
    join_type_cd: Optional[int] = None
    join_index: Optional[int] = None
    join_name: Optional[str] = None
    join_key: Optional[str] = None
    join_desc: Optional[str] = None
    left_data_src_lyt_id: Optional[int] = None
    right_data_src_lyt_id: Optional[int] = None
    left_data_src_id: Optional[int] = None
    right_data_src_id: Optional[int] = None


class JoinOnBase(SQLModel):
    join_on_id: int = Field(default=None, primary_key=True)
    join_on_order: int = Field(..., description="Represents the order of the join")
    left_field_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.layout_fields.lyt_fld_id", description="Represents the left field id")
    right_field_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.layout_fields.lyt_fld_id", description="Represents the right field id")

    # Foreign Keys
    join_id: int = Field(..., foreign_key=f"{Config.DB_SCHEMA}.joins.join_id", description="Represents the join id")


class JoinOn(JoinOnBase, TimestampModel, table=True):
    __tablename__ = "join_on"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    joins: Joins = Relationship(back_populates="join_on")

class JoinOnCreate(JoinOnBase):
    pass


class JoinOnUpdate(SQLModel):
    join_on_order: Optional[int] = None
    left_field_id: Optional[int] = None
    right_field_id: Optional[int] = None
    join_id: Optional[int] = None


class JoinOnReturn(JoinOnBase):
    pass


class JoinsReturn(JoinsBase):
    join_on: Optional[List[JoinOnReturn]] = []
