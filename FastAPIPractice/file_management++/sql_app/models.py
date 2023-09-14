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

    user_dirs = relationship('UserDir', back_populates='owner')
    user_files = relationship('UserFile', back_populates='owner')


class UserDir(Base):
    __tablename__ = 'dirs'

    id = Column(Integer, primary_key=True, index=True)
    dirname = Column(String(length=128), index=True)
    parent_id = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='user_dirs')
    child_files = relationship('UserFile', back_populates='parent')


class UserFile(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(length=128), index=True)
    parent_id = Column(Integer, ForeignKey('dirs.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))

    parent = relationship('UserDir', back_populates='child_files')
    owner = relationship('User', back_populates='user_files')

