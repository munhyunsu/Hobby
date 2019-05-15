import socket
import ssl

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('./server_cert.pem')
    ssock = context.wrap_socket(sock, server_hostname=FLAGS.ip, server_side=False)
    ssock.connect((FLAGS.ip, FLAGS.port))
    print('Connected with server')

    msg = input('Type the message: ')
    msg = msg.encode('utf-8')
    ssock.sendall(msg)
    data = ssock.recv(1500)
    print('Echoed {0}'.format(data.decode('utf-8')))
    ssock.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                        default='localhost')
    parser.add_argument('-p', '--port', type=int,
                        default=8000)
    FLAGS, _ = parser.parse_known_args()

    main(_)
