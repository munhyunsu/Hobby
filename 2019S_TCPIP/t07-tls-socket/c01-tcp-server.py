import socket

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse
    sock.bind(('', FLAGS.port))
    sock.listen(10)
    print('Start tcp echo reverse server')

    while True:
        try:
            print('Waiting client')
            csock, caddr = sock.accept()
            print('Connected with {0}'.format(caddr))
            data = csock.recv(1500)
            print('Received {0} bytes from {1}'.format(len(data), caddr))
            msg = data.decode('utf-8')[::-1].encode('utf-8')
            csock.sendall(msg)
            print('Echoed {0} to {1}'.format(msg, caddr))
            csock.close()
        except KeyboardInterrupt:
            print('Terminated TCP echo reverse server')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--credential',
                        default='credential.csv',
                        help='SHA256 encoded passwords')
    parser.add_argument('-p', '--port',
                        default=8000,
                        help='Serving port number')
    FLAGS, _ = parser.parse_known_args()

    main(_)

