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


def update_is_activate_of_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_file(db: Session, user_id: int, parent_id: int, filename: str):
    db_file = models.UserFile(filename=filename, parent_id=parent_id, owner_id=user_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def read_files_of_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.UserFile).filter(models.UserFile.owner_id == user_id).offset(skip).limit(limit).all()


def get_file_by_id(db: Session, file_id: int):
    return db.query(models.UserFile).filter(models.UserFile.id == file_id).first()


def update_file_location(db: Session, srcfile_id: int, dstdir_id: int):
    db_file = db.query(models.UserFile).filter(models.UserFile.id == srcfile_id).first()
    db_file.parent_id = dstdir_id
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_rootdir(db: Session, user_id: int):
    return db.query(models.UserDir).filter((models.UserDir.owner_id == user_id) & (models.UserDir.parent_id == None)).first()


def get_dir(db: Session, dir_id: int):
    return db.query(models.UserDir).filter(models.UserDir.id == dir_id).first()


def read_dirs_of_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.UserDir).filter(models.UserDir.owner_id == user_id).offset(skip).limit(limit).all()


def get_subdir_by_dirname(db: Session, dirname: str, parent_id: int):
    return db.query(models.UserDir).filter((models.UserDir.dirname == dirname) & (models.UserDir.parent_id == parent_id)).first()


def create_dir(db: Session, user_id: int, dirname: str, parent_id: int | None):
    db_dir = models.UserDir(dirname=dirname, parent_id=parent_id, owner_id=user_id)
    db.add(db_dir)
    db.commit()
    db.refresh(db_dir)
    return db_dir

