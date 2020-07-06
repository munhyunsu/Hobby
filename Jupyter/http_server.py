import http.server
import socketserver

FLAGS = None
_ = None


class HTTPDaemon(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    print(f'Parsed arguments: {FLAGS}')
    print(f'Unparsed arguments: {_}')

    with HTTPDaemon((FLAGS.host, FLAGS.port), 
                    http.server.SimpleHTTPRequestHandler) as httpd:
        print(f'Serving {httpd}')
        httpd.serve_forever()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str,
                        default='')
    parser.add_argument('--port', type=int,
                        default=80)

    FLAGS, _ = parser.parse_known_args()

    main()
