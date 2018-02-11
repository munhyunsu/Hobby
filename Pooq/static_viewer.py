#!/usr/bin/env python3

import sys
import csv


def main(argv):
    rfile = open(argv[1], 'r')
    csv_reader = csv.DictReader(rfile)




# is it good, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
