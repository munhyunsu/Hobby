import datetime

from fastapi.security import OAuth2PasswordBearer
import jwt

from . import conf

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{conf.APP_PREFIX}/token' if conf.APP_PREFIX != '' else 'token',
    auto_error=False
)


def create_jwt(
    data: dict,
    expires_delta: datetime.timedelta | None = None,
):
    to_encode_data = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode_data.update({'exp': expire.timestamp()})
    encoded_jwt = jwt.encode(payload=to_encode_data,
                             key=conf.SECRET_KEY,
                             algorithm=conf.ALGORITHM)
    return encoded_jwt

