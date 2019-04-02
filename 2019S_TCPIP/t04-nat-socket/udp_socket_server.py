import socket

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.ip, FLAGS.port))
    print('Opened UDP echo server')

    while True:
        try:
            data, addr = sock.recvfrom(1560)
            print('Received from {0}'.format(addr))
            sock.sendto(data, addr)
            print('Echo {0} to {1}'.format(data, addr))
        except KeyboardInterrupt:
            print('Terminated UDP echo server')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                         default='')
    parser.add_argument('-p', '--port', type=int,
                         default=6292)

    FLAGS, _ = parser.parse_known_args()
    main(_)

