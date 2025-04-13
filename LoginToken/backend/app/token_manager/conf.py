APP_NAME = 'Token manager'
APP_PREFIX = 'token-manager'
SECRET_KEY = 'This is the secret key. you will need to change this when deploying.'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 2
ACCESS_TOKEN_UNHEALTHY_SECONDS = ACCESS_TOKEN_EXPIRE_SECONDS // 2
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 2 * 2
REFRESH_TOKEN_UNHEALTHY_SECONDS = REFRESH_TOKEN_EXPIRE_SECONDS // 2

try:
    import os
    with open(os.path.join(os.path.dirname(__file__), 'conf_local.py')) as f:
        exec(f.read(), globals())
except IOError:
    pass

