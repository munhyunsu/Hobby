import socket

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((FLAGS.ip, FLAGS.port))
    sock.listen(1)
    print('Opened TCP echo server')

    while True:
        try:
            print('Listening client')
            csock, caddr = sock.accept()
            print('Connected with {0}'.format(caddr))
            data = csock.recv(1500)
            print('Received {0} bytes from {1}'.format(len(data), caddr))
            csock.sendall(data)
            print('Echoed {0} to {1}'.format(data, caddr))
        except KeyboardInterrupt:
            print('Terminated TCP echo server')
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

