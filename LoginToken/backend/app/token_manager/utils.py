import datetime
from typing import Annotated

from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
import jwt

from . import conf, exceptions
from ..user_manager import crud as user_curd

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{conf.APP_PREFIX}/token' if conf.APP_PREFIX != '' else 'token',
    auto_error=False
)


def create_jwt(
    data: dict,
    expires_delta: datetime.timedelta | None = None,
):
    to_encode_data = data.copy()
    if expires_delta is None:
        expires_delta = datetime.timedelta(hours=1)
    expire = datetime.datetime.now(tz=datetime.UTC) + expires_delta
    to_encode_data.update({'exp': expire.timestamp()})
    encoded_jwt = jwt.encode(payload=to_encode_data,
                             key=conf.SECRET_KEY,
                             algorithm=conf.ALGORITHM)
    return encoded_jwt


def decode_access_token(
    access_token: Annotated[str, Depends(oauth2_scheme)],
):
    payload = None
    try:
        payload = jwt.decode(jwt=access_token,
                             key=conf.SECRET_KEY,
                             algorithms=[conf.ALGORITHM])
    except jwt.exceptions.InvalidTokenError:
        pass
    return payload


def verify_access_token(
    access_token: Annotated[str, Depends(oauth2_scheme)],
):
    payload = decode_access_token(access_token)
    if payload is None:
        raise exceptions.CredentialException
    return payload


def decode_refresh_token(
    refresh_token: str = Cookie(None),
):
    payload = None
    try:
        payload = jwt.decode(jwt=refresh_token,
                             key=conf.SECRET_KEY,
                             algorithms=[conf.ALGORITHM])
    except jwt.exceptions.InvalidTokenError:
        pass
    return payload


def verify_refresh_token(
    refresh_token: str = Cookie(None),
):
    payload = decode_refresh_token(refresh_token)
    if payload is None:
        raise exceptions.CredentialException
    return payload

