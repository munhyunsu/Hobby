import datetime

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, plain_password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return False
    if not verify_password(plain_password, db_user.hashed_password):
        return False
    return db_user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_op(db: Session, op: schemas.OpCreate, user_id: int):
    db_op = models.Op(**op.dict(), start_time=datetime.datetime.utcnow(), owner_id=user_id)
    db.add(db_op)
    db.commit()
    db.refresh(db_op)
    return db_op


def get_ops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Op).offset(skip).limit(limit).all()


def get_op(db: Session, op_id: int):
    return db.query(models.Op).filter(models.Op.id == op_id).first()


def get_ops_of_user(db: Session, user_id: int):
    return db.query(models.Op).filter(models.Op.owner_id == user_id).all()

def update_is_activate_of_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
