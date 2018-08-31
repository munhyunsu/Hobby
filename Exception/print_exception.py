#!/usr/bin/env python3

import sys


def raise_exception():
    raise Exception

def main():
    try:
        raise_exception()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
