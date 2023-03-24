import datetime

from pydantic import BaseModel
from typing import Optional


class OpBase(BaseModel):
    pass


class OpCreate(OpBase):
    op: str
    input_var: int


class Op(OpCreate):
    id: int
    start_time: datetime.datetime
    output_var: Optional[int]
    end_time: Optional[datetime.datetime]
    completed: bool
    owner_id: int
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    ops: list[Op] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

