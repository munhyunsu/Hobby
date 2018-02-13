#!/usr/bin/env python3

import sys
import os

import root_lib
from sub import hello


def main(argv):
    print('It is main', os.getcwd())
    hello.hello()
    root_lib.hello()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('It is main', os.getcwd())
    hello.hello()
    root_lib.hello()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
