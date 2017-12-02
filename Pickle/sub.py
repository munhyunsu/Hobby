#!/usr/bin/env python3

import sys
import subprocess

def main(argv):
    subprocess.run(['python3', 'pickle_example.py'])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
