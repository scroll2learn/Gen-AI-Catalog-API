from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.core.config import Config

class CodesHdrBase(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)
    description: str
    type_cd:str


class CodesHdr(CodesHdrBase, table=True):
    __tablename__ = "codes_hdr"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with children
    codes_dtl: Optional[List["CodesDtl"]] = Relationship(back_populates="codes_hdr", sa_relationship_kwargs={"lazy": "selectin"})


class CodesHdrCreate(CodesHdrBase): 
    pass


class CodesHdrUpdate(CodesHdrBase): 
    pass


class CodesDtlBase(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)
    codes_hdr_id: int
    dtl_desc: str
    dtl_id_filter: int

    # Foreign Keys
    codes_hdr_id: Optional[int] = Field(default=None, foreign_key=f"{Config.DB_SCHEMA}.codes_hdr.id")


class CodesDtl(CodesDtlBase, table=True):
    __tablename__ = "codes_dtl"
    __table_args__ = {'schema': Config.DB_SCHEMA}

    # Relationships with Parent
    codes_hdr: Optional[CodesHdr] = Relationship(back_populates="codes_dtl")


class CodesDtlCreate(CodesDtlBase):
    pass


class CodesDtlUpdate(CodesDtlBase):
    pass


class CodesHdrReturn(CodesHdrBase):
    codes_dtl: Optional[List[CodesDtl]] = []


class CodesDtlReturn(CodesDtlBase):
    pass
