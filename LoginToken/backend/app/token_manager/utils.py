from fastapi.security import OAuth2PasswordBearer

from . import conf

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token-manager/token',
    auto_error=False
)


async def create_jwt(
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

