from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):
    identifier: str


class UserScore(User):
    score: list
