from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus
from sqlalchemy.orm import Session

from .. import database
from ..user_manager import schemas as user_schemas, utils as user_utils
from . import schemas

router = APIRouter(
    prefix='/token-manager',
    tags=['Token manager'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('/info', include_in_schema=False)
async def get_info():
    return {'prefix': router.prefix,
            'tags': router.tags,
            'responses': router.responses}


@router.post('/token', response_model=schemas.Token)
async def post_token(
    user: user_schemas.UserLogin,
    db: Session = Depends(database.get_db),
):
    username = user.username.lower()
    password = user.password
    db_user = utils.authenticate_user(db=db, username=username, password=password)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.HTTP_403_FORBIDDEN,
                            detail='Forbidden request')
    return db_user

