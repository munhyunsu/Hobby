FLAGS = None


def main(_):
    print('Parsed, unparsed args {0} {1}'.format(FLAGS, _))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--file1', type=str, required=True,
                        help='File1 for comparison')
    parser.add_argument('-f2', '--file2', type=str, required=True,
                        help='File2 for comparison')
    FLAGS, _ = parser.parse_known_args()

    main(_)

