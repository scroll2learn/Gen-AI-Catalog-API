from sqlmodel import SQLModel, Field

from app.models.base import TimestampModel
from app.core.config import Config


class AppUserBase(SQLModel):
    user_id: int = Field(default=None, nullable=False, primary_key=True)
    email: str = Field(default=None, nullable=False)
    password: str = Field(default=None, nullable=False)
    ad_id: str = Field(default=None, nullable=False,unique=True)
    active : bool = Field(default=True, nullable=False)


class AppUser(AppUserBase, TimestampModel, table=True):
    __tablename__ = "app_user"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class AppUserCreate(AppUserBase): 
    pass


class AppUserUpdate(TimestampModel):
    email: str
    password: str
    ad_id: str


class AppUserReturn(AppUserBase, TimestampModel):
    pass
