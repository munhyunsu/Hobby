import datetime
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .analyzer import lifespan, ops

models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/info/')
def read_info():
    return {'Available ops': list(ops.keys())}


def process_task(db_op: schemas.Op, db: Session = Depends(get_db)):
    if db_op.op in ops.keys():
        ret = ops[db_op.op](db_op.input_var)
        setattr(db_op, 'output_var', ret)
    else:
        setattr(db_op, 'output_var', -1)
    setattr(db_op, 'end_time', datetime.datetime.utcnow())
    setattr(db_op, 'completed', True)
    db.add(db_op)
    db.commit()
    db.refresh(db_op)


@app.get('/op/', response_model=schemas.Op)
def read_op(op_id: int, db: Session = Depends(get_db)):
    op = crud.get_op(db, op_id)
    return op


@app.post('/ops/', response_model=schemas.Op)
def create_op(background_tasks: BackgroundTasks, op: schemas.OpCreate, db: Session = Depends(get_db)):
    db_op = crud.create_op(db=db, op=op)
    background_tasks.add_task(process_task, db_op, db)
    return db_op


@app.get('/ops/', response_model=list[schemas.Op])
def read_ops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ops = crud.get_ops(db, skip=skip, limit=limit)
    return ops

