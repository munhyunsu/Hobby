import re
from pydantic import BaseModel, EmailStr, validator, Field


class UsernameValidatorMixin(BaseModel):
    username: str = Field(min_length=3, max_length=20)

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('username must contain only letters and numbers (no spaces or special characters)')
        return v


class UserBase(UsernameValidatorMixin):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6)
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('password does not match with confirm_password')
        return v


class UserLogin(UsernameValidatorMixin):
    password: str = Field(min_length=6)


class User(UserBase):
    id: int

