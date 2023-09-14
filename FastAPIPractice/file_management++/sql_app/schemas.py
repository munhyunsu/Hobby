import datetime

from pydantic import BaseModel
from typing import Optional


class UserFile(BaseModel):
    id: int
    filename: str
    parent_id: int | None
    owner_id: int

    class Config:
        orm_mode = True


class UserDir(BaseModel):
    id: int
    dirname: str
    parent_id: int | None
    owner_id: int

    child_files: list[UserFile]

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
    user_dirs: list[UserDir]
    user_files: list[UserFile]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

