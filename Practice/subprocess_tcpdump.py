#!/usr/bin/env python3

import sys
import subprocess

def main(argv):
    #proc = subprocess.Popen(['tcpdump'])
    try:
        subprocess.run(['tcpdump', '-l', '-i', 'any'],
                             stdout=subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             universal_newlines = True,
                             timeout=10)
    except subprocess.TimeoutExpired as rtv:
        outs = rtv.stdout
        errs = rtv.stderr

    print(outs)
    print('')
    print(errs)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
