import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

FLAGS = _ = None


def main():
    logging.debug(f'Parsed arguments: {FLAGS}')
    logging.debug(f'Unparsed arguments: {_}')

    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


if __name__ == '__main__':
    os.chdir(sys.path[0])
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')
    parser.add_argument('--input', required=True,
                        help='CSV input (latitude, longitude)')
    parser.add_argument('--output', default=f'kmeans_{int(time.time())}.csv',
                        help='CSV output')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

