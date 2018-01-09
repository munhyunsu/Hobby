#!/usr/bin/env python3

import sys
import logging

FORMAT = '%(created)s:%(levelno)s:%(message)s'
logging.basicConfig(stream = sys.stdout,
                    format = FORMAT,
                    level = logging.DEBUG)

def main(argv):
    if len(argv) < 2:
        logging.debug('We need argument for path')
        return
        
        


# is it good thing, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
