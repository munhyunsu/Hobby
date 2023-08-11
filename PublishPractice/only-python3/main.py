import os
import http
import http.server

FLAGS = _ = None
DEBUG = False


class MyHTTPDaemon(http.server.HTTPServer):
    allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if DEBUG:
            print(f'Client: {self.client_address}')
            print(f'Message: {self.command} {self.path} {self.request_version}')
            print(f'Headers: {self.headers}')

        if not self.path.startswith(FLAGS.prefix):
            return
        self.path = self.path[len(FLAGS.prefix):]
        if self.path == '/':
            path = 'index.html'
        else:
            path = self.path[1:]


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    with MyHTTPDaemon((FLAGS.host, FLAGS.port),
                      MyHTTPRequestHandler) as httpd:
        try:
            print(f'Start HTTP server {httpd.server_address}')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f'Terminate HTTP server {httpd.server_address}')
            httpd.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--host', default='0.0.0.0', type=str,
                        help='The serving IP address')
    parser.add_argument('--port', default=8888, type=int,
                        help='The serving port number')
    parser.add_argument('--prefix', default='', type=str,
                        help='The URL prefix')
    parser.add_argument('--data', default='./data', type=str,
                        help='The web data directory')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
