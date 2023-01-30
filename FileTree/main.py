import config

FLAGS = _ = None
DEBUG = False


def main():
    pass


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--rootfs', default=config.rootfs,
                        help='Root file path')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
