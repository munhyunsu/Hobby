import sys

DEBUG = False


def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'debug':
        DEBUG = True

    main()

