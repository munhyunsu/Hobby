#!/usr/bin/env python3

import sys
import time
import datetime

from adafruit_dht import measure_and_write
from utils import check_internet

def main(argv = sys.argv):
    for index in range(0, 30):
        try:
            measure_and_write()
            return 0
        except Exception as e:
            if index == 29:
                return 1
            print('{0}: Somethine is wrong(loop: {1}, exception: {2})'.format(
                    datetime.datetime.now(),
                    index+1,
                    e))
            time.sleep(60)


if __name__ == '__main__':
    sys.exit(main())
