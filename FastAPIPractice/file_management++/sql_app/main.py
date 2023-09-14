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


def make_dirs(dirfullpath: str):
    os.makedirs(dirfullpath, exist_ok=True)


@app.post('/users/', response_model=schemas.User)
def create_user(
    background_tasks: BackgroundTasks,
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    db_user = crud.create_user(db=db, user=user)
    crud.create_dir(db, db_user.id, '', None)
    fsdirfullpath = os.path.join(FILEROOT, f'{db_user.id}')
    background_tasks.add_task(make_dirs, fsdirfullpath)
    return db_user


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


def save_file(user_id: int, filedir: str, filename: str, file: File()):
    fsfiledir = os.path.join(FILEROOT, f'{user_id}', filedir)
    fsfilepath = os.path.join(fsfiledir, filename)
    with open(fsfilepath, mode='wb') as f:
        f.write(file.file.read())


@app.post('/files/', response_model=schemas.UserFile)
def create_file(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    file: UploadFile,
    dir_id: int = None,
    db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[-1]
    if dir_id is None:
        db_dir = crud.get_rootdir(db, current_user.id)
    else:
        db_dir = crud.get_dir(db, dir_id)
    if db_dir is None or db_dir.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail='No directory linked to dir id')
    filedir = db_dir.dirname
    tmp_db_dir = db_dir
    while True:
        if tmp_db_dir.parent_id is None:
            break
        tmp_db_dir = crud.get_dir(db, tmp_db_dir.parent_id)
        filedir = os.path.join(tmp_db_dir.dirname, filedir)
    while True:
        ruuid = uuid.uuid4()
        filename = f'{ruuid}{ext}'
        fsfiledir = os.path.join(FILEROOT, f'{current_user.id}', filedir)
        fsfilepath = os.path.join(fsfiledir, filename)
        if not os.path.exists(fsfilepath):
            break
    db_file = crud.create_file(db, current_user.id, db_dir.id, filename)
    background_tasks.add_task(save_file, current_user.id, filedir, filename, file)
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
    shutil.move(srcfsfilepath, dstfsfilepath)


@app.put('/files', response_model=schemas.UserFile)
def update_file(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    srcfile_id: int,
    dstdir_id: int = None,
    db: Session = Depends(get_db)):
    db_file = crud.get_file_by_id(db, srcfile_id)
    if db_file is None or db_file.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail='No file linked to file id')
    if dstdir_id is None:
        db_dir = crud.get_rootdir(db, current_user.id)
    else:
        db_dir = crud.get_dir(db, dstdir_id)
    if db_dir is None or db_dir.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail='No directory linked to dir id')
    dstdir_id = db_dir.id

    filedir = db_dir.dirname
    tmp_db_dir = db_dir
    while True:
        if tmp_db_dir.parent_id is None:
            break
        tmp_db_dir = crud.get_dir(db, tmp_db_dir.parent_id)
        filedir = os.path.join(tmp_db_dir.dirname, filedir)
    dstfsfilepath = os.path.join(FILEROOT, f'{db_file.owner_id}', f'{filedir}', f'{db_file.filename}')

    db_dir = crud.get_dir(db, db_file.parent_id)
    filedir = db_dir.dirname
    tmp_db_dir = db_dir
    while True:
        if tmp_db_dir.parent_id is None:
            break
        tmp_db_dir = crud.get_dir(db, tmp_db_dir.parent_id)
        filedir = os.path.join(tmp_db_dir.dirname, filedir)
    srcfsfilepath = os.path.join(FILEROOT, f'{db_file.owner_id}', f'{filedir}', f'{db_file.filename}')

    db_file = crud.update_file_location(db, srcfile_id, dstdir_id)
    background_tasks.add_task(move_file, srcfsfilepath, dstfsfilepath)
    return db_file


@app.get('/dirs/', response_model=list[schemas.UserDir])
def read_dirs(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return crud.read_dirs_of_user(db, current_user.id)


@app.post('/dirs/', response_model=list[schemas.UserDir])
def create_dirs(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    dirpath: str,
    db: Session = Depends(get_db)
    ):
    dirnames = dirpath.split('/')
    dirs = []
    db_dir = crud.get_rootdir(db, current_user.id)
    dirs.append(db_dir)
    for dirname in dirnames:
        next_db_dir = crud.get_subdir_by_dirname(db, dirname, db_dir.id)
        if next_db_dir is None:
            db_dir = crud.create_dir(db, current_user.id, dirname, db_dir.id)
        else:
            db_dir = next_db_dir
        dirs.append(db_dir)
    fsdirfullpath = os.path.join(FILEROOT, f'{current_user.id}', dirpath)
    background_tasks.add_task(make_dirs, fsdirfullpath)
    return dirs
