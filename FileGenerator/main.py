FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--output', type=str, default='output',
                        help='The output file path')
    parser.add_argument('--size', type=int, default=1379*32,
                        help='The output file size')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    DEBUG = FLAGS.debug

    main()
