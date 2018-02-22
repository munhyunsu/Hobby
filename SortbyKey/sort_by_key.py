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

    a2 = {
            'x': {'a': 'a',
                  'b': 'b',
                  'c': 1},
            'y': {'a': 'b',
                  'b': 'c',
                  'c': 2},
            'z': {'a': 'c',
                  'b': 'a',
                  'c': 3}
    }

    a2_2 = [(v['c'], k, v) for k, v in a2.items()]
    print(a2_2)
    a2_2.sort(reverse = True)
    print(a2_2)
    b2 = [(k, v) for c, k ,v in a2_2]
    print(b2)

    print(a2.items())
    print(sorted(a2.items(), key = get_count, reverse = True))
    print(dict(sorted(a2.items(), key = get_count, reverse = True)))

    a3 = [(1, 2), (2, 3), (1, 3)]
    print(dict(a3))

def get_count(x):
    return x[1]['c']


if __name__ == '__main__':
    sys.exit(main(sys.argv))
