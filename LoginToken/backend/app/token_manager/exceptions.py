from fastapi import HTTPException, status


CredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate tokens',
)

