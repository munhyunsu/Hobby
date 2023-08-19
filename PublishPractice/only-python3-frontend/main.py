import os
import json
import time
import http
import http.server
import sqlite3
import urllib
import urllib.request

FLAGS = _ = None
DEBUG = False

CONN = None
CUR = None
EXT = {'.html': 'text/html;charset=utf-8',
       '.js'  : 'text/javascript;charset=utf-8',
       '.css' : 'text/css;charset=utf-8',
       '.jpg' : 'image/jpeg',
       '.jpeg': 'image/jpeg',
       '.png' : 'image/png'}


class MyHTTPDaemon(http.server.HTTPServer):
    allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        global CONN
        global CUR
        if DEBUG:
            print(f'Client: {self.client_address}')
            print(f'Message: {self.command} {self.path} {self.request_version}')
            print(f'Headers: {self.headers}')

        if self.path == '/':
            path = 'index.html'
        else:
            path = self.path[1:]
        path = os.path.join(FLAGS.data, path)
        if DEBUG:
            print(f'Read {path}')
        if not os.path.exists(path):
            self.send_error(http.HTTPStatus.NOT_FOUND, 'Not Found')
            return
        ext = os.path.splitext(path)[-1].lower()
        self.send_response(http.HTTPStatus.OK)
        if ext in EXT.keys():
            self.send_header('Content-Type', EXT[ext])
        else:
            self.send_header('Content-Type', 'application/octet-stream')

        content = ''

        with open(path, 'rb') as f:
            body = f.read()
            body = body.replace('{{PREFIX}}'.encode('utf-8'), 
                                f'{FLAGS.prefix}'.encode('utf-8'))
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        global CONN
        global CUR
        if DEBUG:
            print(f'Client: {self.client_address}')
            print(f'Message: {self.command} {self.path} {self.request_version}')
            print(f'Headers: {self.headers}')
            print(f'Body: {body}')

        if self.path == '/index.html':
            body = self.rfile.read(int(self.headers['Content-Length']))
            body = urllib.parse.parse_qs(body.decode('utf-8'))
            data = {'username': body['username'][0],
                    'content': body['content'][0]}
            data = json.dumps(data)
            data = data.encode('utf-8')
            with urllib.request.urlopen(f'http://{FLAGS.backhost}:{FLAGS.backport}{FLAGS.backprefix}',
                                        data) as f:
                res = f.read().decode('utf-8')
            self.send_response(http.HTTPStatus.FOUND, 'Found')
            self.send_header('Location', f'{self.path}')
            self.end_headers()
        else:
            self.send_response(http.HTTPStatus.NOT_FOUND, 'Not Found')
            self.end_headers()


def main():
    global CONN
    global CUR

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
    parser.add_argument('--port', default=10001, type=int,
                        help='The serving port number')
    parser.add_argument('--prefix', default='/paste', type=str,
                        help='The URL prefix')
    parser.add_argument('--data', default='./data', type=str,
                        help='The web data directory')
    parser.add_argument('--backhost', default='0.0.0.0', type=str,
                        help='The backend server IP address')
    parser.add_argument('--backport', default=10002, type=int,
                        help='The backend server port')
    parser.add_argument('--backprefix', default='/paste/api/v1', type=str,
                        help='The backend server prefix')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()
