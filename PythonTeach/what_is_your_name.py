#!/usr/bin/env python3

import sys

def main(argv):
    name = input('이름이 무엇인가요? ')
    print('안녕하세요! {}'.format(name))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
