import os
import struct

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    div = int.from_bytes(b'\xff', byteorder='big')+1
    with open(FLAGS.output, 'wb') as f:
        for row in range(FLAGS.size):
            i = row%div
            if DEBUG:
                data = struct.pack('>B', i)
                print(f'{i} {data.hex()}*{FLAGS.chunk}')
            for col in range(FLAGS.chunk):
                f.write(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--output', type=str, default='output',
                        help='The output file path')
    parser.add_argument('--size', type=int, default=32,
                        help='The number of chunk')
    parser.add_argument('--chunk', type=int, default=1379,
                        help='The unit size')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    DEBUG = FLAGS.debug

    main()
