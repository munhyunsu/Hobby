import socket
import time

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
            if data.decode('utf-8') == 'p':
                print('Wait for client close socket')
                while csock.recv(1500).decode('utf-8') != '':
                    time.sleep(0.5)
                    pass
                print('Sleep 5 seconds before socket close')
                print('Check the CLOSE_WAIT state')
                time.sleep(5)
                csock.close()
            elif data.decode('utf-8') == 'a':
                print('Close client socket server first')
                csock.close()
            print('Closed connection with {0}'.format(caddr))
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


