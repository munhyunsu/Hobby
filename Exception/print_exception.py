#!/usr/bin/env python3

import sys
import traceback

def raise_exception():
    raise Exception

def main():
    try:
        raise_exception()
    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()
