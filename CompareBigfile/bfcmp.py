import csv

FLAGS = None


def read_data(path):
    addresses = set()
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            addresses.add(row[0])
    return addresses


def compare_sets(path1, path2):
    set_a = read_data(path1)
    set_b = read_data(path2)
    set_a_only = set_a - set_b
    set_b_only = set_b - set_a
    set_ab_both = set_a & set_b
    print('{0} size : {1}'.format(path1, len(set_a)))
    print('{0} size : {1}'.format(path2, len(set_b)))
    print('{0} only : {1}'.format(path1, len(set_a_only)))
    print('{0} only : {1}'.format(path2, len(set_b_only)))
    print('{0} and {1} both: {2}'.format(path1, path2, len(set_ab_both)))


def main(_):
    print('Parsed, unparsed args {0} {1}'.format(FLAGS, _))

    compare_sets(FLAGS.f1, FLAGS.f2)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--file1', type=str, required=True,
                        help='File1 for comparison')
    parser.add_argument('-f2', '--file2', type=str, required=True,
                        help='File2 for comparison')
    FLAGS, _ = parser.parse_known_args()

    main(_)

