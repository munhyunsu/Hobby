from data import data_handler
from interface import cli

ARGS = None

class Manager(object):
    def __init__(self, path):
        self.data = data_handler.load(path)

    def start(self):
        cli.intro()
        print(self.data)


def main():
    manager = Manager(ARGS.data)
    manager.start()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, 
                        default='data.json',
                        help='The json file for archving data')
    parser.add_argument('-u', '--user', type=str,
                        required=True,
                        help='The csv file from deckshop.pro')

    ARGS = parser.parse_args()

    main()

