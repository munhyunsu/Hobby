import os
import csv
from operator import itemgetter


FLAGS = None
_ = None


def main():
    results = dict()
    with open(FLAGS.input, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            name1 = os.path.basename(row[0])
            name2 = os.path.basename(row[1])
            if not name1 == name2:
                continue
            sim = int(row[2][:-1])
            result = results.get(name1, list())
            result.append((row[0], row[1], sim))
            results[name1] = result

    for key, result in results.items():
       result.sort(key=itemgetter(2), reverse=True)

    with open(FLAGS.output, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL,
                            lineterminator=os.linesep)
        for key, result in results.items():
            for row in result:
                writer.writerow(row)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file')
    parser.add_argument('-o', '--output', type=str,
                        default='./output.txt',
                        help='Output file')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    main()
