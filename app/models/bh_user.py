from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON

from app.models.base import TimestampModel
from app.core.config import Config


class BHUserBase(SQLModel):
    bh_user_id: int = Field(default=None, primary_key=True)
    bh_user_first_name: str = Field(..., description="The user first name for the project")
    bh_user_middle_name: str = Field(..., description="The user middle name for the project")
    bh_user_last_name: str = Field(..., description="The user last name for the project")
    user_email_id: str = Field(..., description="The user email for the project")
    user_status_cd: int = Field(..., description="The user status for the project")
    user_admin_status_cd: int = Field(..., description="The user admin or not for the project")
    project_details: list = Field(sa_column=Column(JSON), description="project details and role detail")


class BHUser(BHUserBase, TimestampModel, table=True):
    __tablename__ = "bh_user"
    __table_args__ = {'schema': Config.DB_SCHEMA}


class BHUserCreate(BHUserBase): 
    pass


class BHUserUpdate(TimestampModel):
    bh_user_first_name: str
    bh_user_middle_name: str
    bh_user_last_name: str
    user_email_id: str
    user_status_cd: int 
    user_admin_status_cd: int 
    project_details: list 


class BHUserReturn(BHUserBase, TimestampModel):
    pass
