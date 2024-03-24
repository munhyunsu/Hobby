from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):
    identifier: str


class UserScore(User):
    number: int | None = None
    score: dict

