#!/usr/bin/env python3

import sys

from adafruit_dht import measure_and_write


def main(argv = sys.argv):
    measure_and_write()

if __name__ == '__main__':
    sys.exit(main())
