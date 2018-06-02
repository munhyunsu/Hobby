#!/usr/bin/env python3

import sys

from adafruit_dht import measure_and_write
from utils import check_internet

def main(argv = sys.argv):
    if not check_internet:
        sys.exit(0)

    measure_and_write()

if __name__ == '__main__':
    sys.exit(main())
