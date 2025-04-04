from sqlalchemy.orm import Session

from . import models, enums


def select_users(db: Session, sort: enums.UserSortOrder, offset: int, limit: int):
    order_by = models.User.id.asc() if sort == enums.UserSortOrder.asc else models.User.id.desc()
    return db.query(models.User).order_by(order_by).offset(offset).limit(limit).all()


def select_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def select_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def insert_user(db: Session, username: str, email: str, hashed_password: str):
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

