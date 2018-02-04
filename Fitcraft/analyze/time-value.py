#!/usr/bin/env python3

import sys
import matplotlib
import sqlite

DBCONN = None

def main(argv):
    pass

def get_database():
    if DBCONN == None:
        DBCONN = sqlite.connect('fitcraft.sqlite')
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
