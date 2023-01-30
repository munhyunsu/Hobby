import os
import json
import pprint

import config

FLAGS = _ = None
DEBUG = False


def main():
    print(f'Parsed arguments: {FLAGS}')
    print(f'Unparsed arguments: {_}')

    rootfs = os.path.expanduser(os.path.abspath(FLAGS.rootfs))
    tree = [{'type': 'd',
             'name': os.path.relpath(rootfs, rootfs),
             'child': []}]
    queue = [(rootfs, tree[0])]

    while len(queue):
        cpath, node = queue.pop(0)
        with os.scandir(cpath) as it:
            for entry in it:
                if entry.name.startswith('.'):
                    continue
                if entry.is_dir():
                    leaf = {'type': 'd',
                            'name': os.path.relpath(entry.path, rootfs),
                            'child': []}
                    node['child'].append(leaf)
                    queue.append((entry.path, leaf))
                elif entry.is_file():
                    leaf = {'type': 'f',
                            'name': os.path.relpath(entry.path, rootfs),
                            'child': []}
                    node['child'].append(leaf)

    print(json.dumps(tree))


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--rootfs', default=config.rootfs,
                        help='Root file path')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
