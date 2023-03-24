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

    ops = relationship('Op', back_populates='owner')


class Op(Base):
    __tablename__ = 'ops'

    id = Column(Integer, primary_key=True, index=True)
    op = Column(String(length=64))
    input_var = Column(Integer)
    start_time = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    output_var = Column(Integer, nullable=True)
    end_time = Column(DateTime(timezone=False), nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='ops')

