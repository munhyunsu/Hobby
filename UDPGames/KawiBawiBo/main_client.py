import os
import socket
import random

FLAGS = _ = None
DEBUG = False

HANDS = ['Kawi', 'Bawi', 'Bo', 'kawi', 'bawi', 'bo']
ERROR = ['A', 'B', 'C', 'D', 'E', 'F']

def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pid = os.getpid()
    message = f'{pid}'
    hand_count = random.randint(1, 10)
    if pid%10 == 0:
        candidate = HANDS + ERROR
    else:
        candidate = HANDS
    for hand in random.choices(candidate, k=hand_count):
        message = f'{message} {hand}'

    sock.sendto(message.encode('utf-8'), (FLAGS.address, FLAGS.port))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=6292+2022,
                        help='The poort to serve service')
    parser.add_argument('--input', type=str, default=f'{os.getpid()}',
                        help='The message for send')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

