import socket

FLAGS = None


def main(_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((FLAGS.ip, FLAGS.port))
    print('Connected with server')

    msg = input('Type the message: ')
    msg = msg.encode('utf-8')
    sock.sendall(msg)
    data = sock.recv(1500)
    print('Echoed {0}'.format(data.decode('utf-8')))
    sock.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                        default='localhost')
    parser.add_argument('-p', '--port', type=int,
                        default=8000)
    FLAGS, _ = parser.parse_known_args()

    main(_)

