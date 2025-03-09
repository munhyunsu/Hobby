import datetime

DEVMODE = False
URLPREFIX = ''
ORIGINS = [
]
TIMEZONE = datetime.timezone(datetime.timedelta(hours=0))

try:
    import os
    with open(os.path.join(os.path.dirname(__file__), 'conf_local.py')) as f:
        exec(f.read(), globals())
except IOError:
    pass

