import os
import datetime
import uuid
import shutil

from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, status, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from . import crud, models, schemas
from .database import SessionLocal, engine
from .analyzer import lifespan
from .conf import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FILEROOT

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI(lifespan=lifespan)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/token', response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me/', response_model=schemas.User)
def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@app.post('/users/activate/', response_model=schemas.User)
def update_is_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return crud.update_is_activate_of_user(db, current_user.id)


def save_file(user_id: int, dbfiledir: str, filename: str, file: File()):
    fsfiledir = os.path.join(FILEROOT, f'{user_id}', dbfiledir)
    os.makedirs(fsfiledir, exist_ok=True)
    fsfilepath = os.path.join(fsfiledir, filename)
    with open(fsfilepath, mode='wb') as f:
        f.write(file.file.read())


@app.post('/files/', response_model=schemas.UserFile)
def create_file(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    file: UploadFile,
    filedir: str = '',
    db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[-1]
    while True:
        ruuid = uuid.uuid4()
        filename = f'{ruuid}{ext}'
        fsfiledir = os.path.join(FILEROOT, f'{current_user.id}', filedir)
        fsfilepath = os.path.join(fsfiledir, filename)
        if not os.path.exists(fsfilepath):
            break
    dbfiledir = os.path.join(filedir)
    db_file = crud.create_file(db, current_user.id, dbfiledir, filename)
    background_tasks.add_task(save_file, current_user.id, dbfiledir, filename, file)
    return db_file


@app.get('/files/', response_model=list[schemas.UserFile])
def read_files(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return crud.read_files_of_user(db, current_user.id)


def move_file(srcfsfilepath: str, dstfsfilepath: str):
    dstfsfiledir = os.path.dirname(dstfsfilepath)
    os.makedirs(dstfsfiledir, exist_ok=True)
    shutil.move(srcfsfilepath, dstfsfilepath)


@app.put('/files', response_model=schemas.UserFile)
def update_file(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    srcfileid: int,
    dstfiledir: str,
    db: Session = Depends(get_db)):
    db_file = crud.get_file_by_id(db, srcfileid)
    if db_file is None or db_file.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail='No file linked to file id')
    srcfsfilepath = os.path.join(FILEROOT, f'{db_file.owner_id}', f'{db_file.filedir}', f'{db_file.filename}')
    dstfsfilepath = os.path.join(FILEROOT, f'{db_file.owner_id}', f'{dstfiledir}', f'{db_file.filename}')
    db_file = crud.update_file_location(db, srcfileid, dstfiledir)
    background_tasks.add_task(move_file, srcfsfilepath, dstfsfilepath)
    return db_file
