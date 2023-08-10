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
    parser.add_argument('--host', default='0.0.0.0', type=str,
                        help='The serving IP address')
    parser.add_argument('--port', default=8888, type=int,
                        help='The serving port number')
    parser.add_argument('--prefix', default='', type=str,
                        help='The URL prefix')
    parser.add_argument('--data', default='./data', type=str,
                        help='The web data directory')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
