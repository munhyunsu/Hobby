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
    
    class Config:
        orm_mode = True

