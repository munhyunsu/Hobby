FLAGS = None


def read_data(path, col_num, col_name):
    # TODO: Read data from csv by col_num | col_name exclusive
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

