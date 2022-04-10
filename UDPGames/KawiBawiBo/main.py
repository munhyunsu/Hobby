import threading
import socketserver

FLAGS = _ = None
DEBUG = False

class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        print(rfile, wfile)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    
    server = ThreadedUDPServer((FLAGS.address, FLAGS.port),
                               ThreadedUDPRequestHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        try:
            server_thread.start()
        except KeyboardInterrupt:
            server.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=6292+2022,
                        help='The poort to serve service')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

