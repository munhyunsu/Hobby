from sqlalchemy.orm import Session

from . import crud


def validate_user(db: Session, username: str, password: str):
    db_user = crud.select_user_by_username(db=db, username=username)
    if user and pwd_context.verify(password, db_user.hashed_password):
        return user
    return None

