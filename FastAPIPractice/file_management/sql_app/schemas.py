import datetime

from pydantic import BaseModel
from typing import Optional


class UserFile(BaseModel):
    id: int
    owner_id: int
    filedir: str
    filename: str

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
    user_files: list[UserFile]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


