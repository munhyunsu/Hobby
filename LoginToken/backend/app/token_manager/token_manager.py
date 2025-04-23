import datetime
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus, Request, Response, Form
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


@router.get('/token/decode')
async def get_token_decode(
    access_token: Annotated[dict, Depends(utils.verify_access_token)],
    refresh_token: Annotated[dict, Depends(utils.verify_refresh_token)],
):
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/token')
async def get_token(
    access_token_payload: Annotated[str, Depends(utils.decode_access_token)],
    refresh_token_payload: Annotated[str, Depends(utils.decode_refresh_token)],
):
    return access_token_payload, refresh_token_payload


@router.post('/token', response_model=schemas.Token)
async def post_token(
    request: Request,
    response: Response,
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

    refresh_expires_delta = datetime.timedelta(
        seconds=conf.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = utils.create_jwt(
        data={'sub': db_user.username},
        expires_delta=refresh_expires_delta
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        max_age=conf.REFRESH_TOKEN_EXPIRE_SECONDS,
        secure=conf.COOKIE_SECURE,
        samesite='lax',
        path=conf.COOKIE_PATH,
    )

    return {'token_type': 'bearer', 'access_token': access_token}


@router.get('/is-healthy')
async def is_healthy(
    access_token_payload: Annotated[dict, Depends(utils.verify_access_token)],
    refresh_token_payload: Annotated[dict, Depends(utils.verify_refresh_token)],
):
    now = datetime.datetime.now(tz=datetime.UTC).timestamp()

    access_exp = access_token_payload.get('exp', 0)
    access_remaining = access_exp - now
    access_healthy = access_remaining > conf.ACCESS_TOKEN_UNHEALTHY_SECONDS

    refresh_exp = refresh_token_payload.get('exp', 0)
    refresh_remaining = refresh_exp - now
    refresh_healthy = refresh_remaining > conf.REFRESH_TOKEN_UNHEALTHY_SECONDS

    return {
        'access_token': {
            'is_healthy': access_healthy,
            'remaining_seconds': access_remaining
        },
        'refresh_token': {
            'is_healthy': refresh_healthy,
            'remaining_seconds': refresh_remaining
        }
    }


@router.post('/renew/access_token', response_model=schemas.Token)
def renew_access_token(
    access_token: Annotated[dict, Depends(utils.verify_access_token)],
):
    username = access_token.get('sub')
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized access token')

    now = datetime.datetime.now(tz=datetime.UTC).timestamp()
    exp = access_token.get('exp', 0)
    remaining = exp - now

    if remaining > conf.ACCESS_TOKEN_UNHEALTHY_SECONDS:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='Access token still healthy')

    access_expires_delta = datetime.timedelta(
        seconds=conf.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    access_token = utils.create_jwt(
        data={'sub': username},
        expires_delta=access_expires_delta
    )

    return {'token_type': 'bearer', 'access_token': access_token}


@router.post('/renew/refresh_token', response_model=schemas.Token)
def renew_refresh_token(
    response: Response,
    refresh_token: Annotated[dict, Depends(utils.verify_refresh_token)],
):
    username = refresh_token.get('sub')
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized refresh token')

    now = datetime.datetime.now(tz=datetime.UTC).timestamp()
    exp = refresh_token.get('exp', 0)
    remaining = exp - now

    if remaining > conf.REFRESH_TOKEN_UNHEALTHY_SECONDS:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail='Refresh token still healthy')

    access_expires_delta = datetime.timedelta(
        seconds=conf.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    access_token = utils.create_jwt(
        data={'sub': username},
        expires_delta=access_expires_delta
    )

    refresh_expires_delta = datetime.timedelta(
        seconds=conf.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = utils.create_jwt(
        data={'sub': username},
        expires_delta=refresh_expires_delta
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        max_age=conf.REFRESH_TOKEN_EXPIRE_SECONDS,
        secure=conf.COOKIE_SECURE,
        samesite='lax',
        path=conf.COOKIE_PATH,
    )

    return {'token_type': 'bearer', 'access_token': access_token}

