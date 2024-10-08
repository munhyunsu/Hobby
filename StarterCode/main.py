import logging

FLAGS = _ = None


def main():
    logging.critical('Critical message example')
    logging.error('Error message example')
    logging.warning('Warning message example')
    logging.info('Info message example')
    logging.debug('Debug message example')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

