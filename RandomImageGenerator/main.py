import csv

from PIL import Image, ImageFont, ImageDraw

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    print(f'Salt: {FLAGS.salt}')




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', required=True,
                        help='The input csv file for members')
    parser.add_argument('--salt', default=random.getrandbits(64),
                        help='The salt number')
    parser.add_argument('--width', default=800,
                        help='The width')
    parser.add_argument('--height', default=600,
                        help='The height')
    parser.add_argument('--output', default='output',
                        help='The output directory')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    DEBUG = FLAGS.debug

    main()
