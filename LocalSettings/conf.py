import os

VAR1 = 'VAR1 of conf.py'
VAR2 = 'VAR2 of conf.py'


try:
    with open(os.path.join(os.path.dirname(__file__), 'local_conf.py')) as f:
        exec(f.read(), globals())
except IOError:
    pass
