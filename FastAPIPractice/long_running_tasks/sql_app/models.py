import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.orm import relationship

from .database import Base


class Op(Base):
    __tablename__ = 'ops'

    id = Column(Integer, primary_key=True, index=True)
    op = Column(String(length=64))
    input_var = Column(Integer)
    start_time = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    output_var = Column(Integer, nullable=True)
    end_time = Column(DateTime(timezone=False), nullable=True)
    completed = Column(Boolean, default=False)

