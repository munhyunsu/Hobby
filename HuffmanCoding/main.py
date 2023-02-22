import os
import csv
import collections
import operator

FLAGS = _ = None
DEBUG = False


class Node():
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return f'{self.key} {self.value} ({self.left is not None}, {self.right is not None})'


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    data = []
    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = Node(row['Key'], float(row['Ratio']))
            data.append(node)
    data.sort(reverse=True)
    if DEBUG:
        print('Readed Data:')
        for d in data:
            print(d)

    while len(data) > 1:
        l1 = data.pop()
        l2 = data.pop()
        node = Node(f'{l2.key}-{l1.key}', l2.value+l1.value, l2, l1)
        data.append(node)
        data.sort(reverse=True)
        if DEBUG:
            print(f'Building Huffman Binary Tree... (Top Node: {len(data)})')
            for d in data:
                print(d)

    if DEBUG:
        print('Creating Huffman Code...')
    stack = []
    stack.append((data.pop(), ''))
    huffman = dict()
    while len(stack) != 0:
        node, code = stack.pop()
        if node.left is None and node.right is None:
            huffman[node.key] = code
            if DEBUG:
                print(f'{node.key}: {code}')
            continue
        if node.right is not None:
            next_code = f'{code}1'
            stack.append((node.right, next_code))
        if node.left is not None:
            next_code = f'{code}0'
            stack.append((node.left, next_code))

    print('Huffman Code:')
    data = []
    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row['Key'], float(row['Ratio'])))
    data.sort(key=operator.itemgetter(1), reverse=True)
    for key, value in data:
        print(f'{key}: {huffman[key]}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', required=True,
                        help='The input csv file')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main()
