from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import crud

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def validate_user(db: Session, username: str, password: str):
    db_user = crud.select_user_by_username(db=db, username=username)
    if db_user and pwd_context.verify(password, db_user.hashed_password):
        return db_user
    return None

