import conf
from conf import *

VAR1 = 'VAR1 of main.py'


def main():
    print(__file__, VAR1)
    print(__file__, VAR2)
    print(__file__, conf.VAR1)
    print(__file__, conf.VAR2)


if __name__ == '__main__':
    main()

