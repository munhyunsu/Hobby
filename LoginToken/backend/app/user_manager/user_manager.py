from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus
from sqlalchemy.orm import Session

from .. import database
from . import models, schemas, crud, enums, utils


models.database.Base.metadata.create_all(bind=database.engine)

router = APIRouter(
    prefix='/user-manager',
    tags=['User manager'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('/info', include_in_schema=False)
async def get_info():
    return {'prefix': router.prefix,
            'tags': router.tags,
            'responses': router.responses}


@router.get('/users', response_model=list[schemas.User])
async def get_users(
    sort: enums.UserSortOrder = enums.UserSortOrder.asc,
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
):
    return crud.select_users(db=db, sort=sort, offset=offset, limit=limit)


@router.post('/user', response_model=schemas.User)
async def post_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
):
    username = user.username.lower()
    if crud.select_user_by_username(db=db, username=username):
        raise HTTPException(status_code=HTTPStatus.HTTP_409_CONFLICT,
                            detail='This username is already registered')
    email = user.email.lower()
    if crud.select_user_by_email(db=db, email=email):
        raise HTTPException(status_code=HTTPStatus.HTTP_409_CONFLICT,
                            detail='This email is already registered')

    hashed_password = utils.pwd_context.hash(user.password)
    db_user = crud.insert_user(
        db=db,
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    return db_user


## 이 함수는 사용되지 않음! 그냥 연습용!
@router.post('/login', response_model=schemas.User)
async def post_login(
    user: schemas.UserLogin,
    db: Session = Depends(database.get_db),
):
    username = user.username.lower()
    password = user.password
    db_user = utils.validate_user(db=db, username=username, password=password)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.HTTP_403_FORBIDDEN,
                            detail='Forbidden request')
    return db_user

