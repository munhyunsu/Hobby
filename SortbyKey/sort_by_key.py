#!/usr/bin/env python3

import sys
from operator import itemgetter

def main(argv):
    a = [
            {'a': 'a',
             'b': 'b',
             'c': 'c'},
            {'a': 'b',
             'b': 'c',
             'c': 'a'},
            {'a': 'c',
             'b': 'a',
             'c': 'b'}
    ]

    b = sorted(a, key = itemgetter('c'))

    print(a)
    print(b)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
