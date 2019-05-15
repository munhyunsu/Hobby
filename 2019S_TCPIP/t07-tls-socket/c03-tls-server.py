import socket
import ssl

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse
    sock.bind(('localhost', FLAGS.port))
    sock.listen(10)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(FLAGS.cert, FLAGS.key)

    ssock = context.wrap_socket(sock, server_side=True)

    print('Start tcp echo reverse server')

    while True:
        try:
            print('Waiting client')
            csock, caddr = ssock.accept()
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
    parser.add_argument('-p', '--port', type=int,
                        default=8000,
                        help='Serving port number')
    parser.add_argument('-c', '--cert',
                        required=True,
                        help='Server certificate file path')
    parser.add_argument('-k', '--key',
                        required=True,
                        help='Server key file path')
    FLAGS, _ = parser.parse_known_args()

    main(_)

