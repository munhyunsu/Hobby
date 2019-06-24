import csv

FLAGS = None


def comset(seta, setb):
    # TODO: compare set a and set b
    pass


def read_data(path, col_num=None, col_name=None):
    # Set pivot where is data located
    if (col_num is not None) and (col_name is not None):
        print('Error! only one of col_num or col_name should be provided')
        return
    if col_num is not None:
        col = col_num
    elif col_name is not None:
        col = col_name
    data = set()
    pass


def _read_data_num(path, col):
    pass


def _read_data_col(path, col):
    pass


def main(_):
    print('Parsed, unparsed args {0} {1}'.format(FLAGS, _))

    # TODO: Read first column data from each csv files


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--file1', type=str, required=True,
                        help='File1 for comparison')
    parser.add_argument('-f2', '--file2', type=str, required=True,
                        help='File2 for comparison')
    FLAGS, _ = parser.parse_known_args()

    main(_)

