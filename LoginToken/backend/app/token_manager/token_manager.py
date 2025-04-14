import datetime
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus, Request, Form
from sqlalchemy.orm import Session

from .. import database
from ..user_manager import schemas as user_schemas, utils as user_utils
from . import conf, schemas, utils

router = APIRouter(
    prefix=f'/{conf.APP_PREFIX}' if conf.APP_PREFIX != '' else f'{conf.APP_PREFIX}',
    tags=[f'{conf.APP_NAME}'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('/info', include_in_schema=False)
async def get_info():
    return {'prefix': router.prefix,
            'tags': router.tags,
            'responses': router.responses}


@router.get('/token')
async def get_token(
    access_token: Annotated[str, Depends(utils.decode_access_token)],
    refresh_token: Annotated[str, Depends(utils.decode_refresh_token)],
):
    return access_token, refresh_token


@router.post('/token', response_model=schemas.Token)
async def post_token(
    request: Request,
    db: Session = Depends(database.get_db),
):
    content_type = request.headers.get('content-type', '').lower()

    if 'application/json' in content_type:
        body = await request.json()
        username = body.get('username', '').lower()
        password = body.get('password', '')
    elif 'application/x-www-form-urlencoded' in content_type:
        form = await request.form()
        username = form.get('username', '').lower()
        password = form.get('password', '')
    else:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
            detail='Unsupported Content-Type. Use \'application/json\' or \'application/x-www-form-urlencoded\'',
        )

    db_user = user_utils.authenticate_user(db=db, username=username, password=password)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    access_expires_delta = datetime.timedelta(
        seconds=conf.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    access_token = utils.create_jwt(
        data={'sub': db_user.username},
        expires_delta=access_expires_delta
    )
    return {'token_type': 'bearer', 'access_token': access_token}



