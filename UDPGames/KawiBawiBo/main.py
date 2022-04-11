import threading
import socketserver

FLAGS = _ = None
DEBUG = False


class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        message = self.rfile.read().decode('utf-8')
        print(f'{message} from {self.client_address}')
        data = message.encode('utf-8')
        self.wfile.write(data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    
    server = ThreadedUDPServer((FLAGS.address, FLAGS.port),
                               ThreadedUDPRequestHandler)
    server.allow_reuse_address = True

    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        try:
            server_thread.start()
            server_thread.join()
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

