#!/usr/bin/env python3

import sys
import subprocess
import urllib.request
import copy

def main(argv):
    cookie = urllib.request.HTTPCookieProcessor()
    oc = copy.deepcopy(cookie)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
