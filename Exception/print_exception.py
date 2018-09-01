#!/usr/bin/env python3

import sys
import traceback

def raise_exception():
    raise Exception

def main():
    try:
        raise_exception()
    except Exception as e:
        #traceback.print_exc()
        trace_string = traceback.format_exc()
        print(trace_string)

if __name__ == '__main__':
    main()
