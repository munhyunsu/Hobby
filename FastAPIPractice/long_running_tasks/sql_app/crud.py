import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def create_op(db: Session, op: schemas.OpCreate):
    db_op = models.Op(**op.dict(), start_time=datetime.datetime.utcnow())
    db.add(db_op)
    db.commit()
    db.refresh(db_op)
    return db_op


def get_ops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Op).offset(skip).limit(limit).all()


def get_op(db: Session, op_id: int):
    return db.query(models.Op).filter(models.Op.id == op_id).first()

