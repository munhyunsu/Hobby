import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=64), unique=True, index=True)
    email = Column(String(length=128), unique=True, index=True)
    hashed_password = Column(String(length=128))
    is_active = Column(Boolean, default=False)

