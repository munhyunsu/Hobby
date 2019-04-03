import socket

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    print('Opened UDP echo client')

    while True:
        try:
            msg = input('Type the message: ')
            msg = msg.encode('utf-8')
            sock.sendto(msg, (FLAGS.ip, FLAGS.port))
            data, addr = sock.recvfrom(1560)
            print('Echoed {0} from {1}'.format(data, addr))
        except KeyboardInterrupt:
            print('Terminated UDP echo client')
            break
        except socket.timeout:
            print('Server is not responding')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                         default='localhost')
    parser.add_argument('-p', '--port', type=int,
                         default=6292)

    FLAGS, _ = parser.parse_known_args()
    main(_)

