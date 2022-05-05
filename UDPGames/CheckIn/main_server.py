import os
import csv
import socket

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    verifier = set()
    with open(FLAGS.verify, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            verifier.add(int(row[0]))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    print(f'Start CheckIn')

    while True:
        data, client = sock.recvfrom(2**16)
        data = data.decode('utf-8')
        try:
            data = int(data)
        except ValueError:
            pass
        if data in verifier:
            print(f'CheckIn {data}')
            sock.sendto('CheckIn'.encode('utf-8'), client)
        else:
            sock.sendto('Error'.encode('utf-8'), client)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='0.0.0.0',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=38442,
                        help='The port to serve service')
    parser.add_argument('--verify', type=str, default='verify.csv',
                        help='The student number csv file')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    FLAGS.verify = os.path.abspath(os.path.expanduser(FLAGS.verify))

    main()

