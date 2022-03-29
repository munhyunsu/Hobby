import os
import collections
import operator

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    with open(FLAGS.input, 'rb') as f:
        data = f.read()

    counter = collections.Counter(data.hex())
    total = sum(counter.values())
    print('HexString Ratio Counts')
    for key, value in sorted(counter.items(), key=operator.itemgetter(1), reverse=True):
        if DEBUG:
            print(f'{key.upper()}: {value/total:>} {value:>}')
        else:
            print(f'{key.upper()}: {value/total:>.10f} {value:>10d}')





if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', required=True,
                        help='The input file')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main()
