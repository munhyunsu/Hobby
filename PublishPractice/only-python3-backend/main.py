import os
import json
import time
import http
import http.server
import sqlite3
import urllib

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

        if not self.path.startswith(FLAGS.prefix):
            return
        self.path = self.path[len(FLAGS.prefix):]
        if self.path == '/paste':
            data = {'Pastes': []}
            CUR.execute('''SELECT user, content
                           FROM Paste
                           ORDER BY id DESC;''')
            for row in CUR:
                data['Pastes'].append({'User': row[0],
                                          'Content': row[1]})

            body = json.dumps(data)
            body = body.encode('utf-8')
        else:
            return

        self.send_response(http.HTTPStatus.OK, 'OK')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)


    def do_POST(self):
        global CONN
        global CUR
        body = self.rfile.read(int(self.headers['Content-Length']))
        if DEBUG:
            print(f'Client: {self.client_address}')
            print(f'Message: {self.command} {self.path} {self.request_version}')
            print(f'Headers: {self.headers}')
            print(f'Body: {body}')
        data = json.loads(body.decode('utf-8'))

        CUR.execute('''INSERT INTO Paste (user, utime, content) 
                         VALUES (?, ?, ?);''',
                    (data['username'], int(time.time()), data['content']))
        CONN.commit()

        self.send_response(http.HTTPStatus.CREATED, 'Created')
        self.end_headers()


def main():
    global CONN
    global CUR

    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    CONN = sqlite3.connect(FLAGS.database)
    CUR = CONN.cursor()
    CUR.execute('''CREATE TABLE IF NOT EXISTS Paste (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user TEXT NOT NULL,
                     utime INTEGER NOT NULL,
                     content TEXT);''')
    CONN.commit()

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
    parser.add_argument('--port', default=10002, type=int,
                        help='The serving port number')
    parser.add_argument('--prefix', default='/paste/api/v1', type=str,
                        help='The URL prefix')
    parser.add_argument('--database', default='./main.db', type=str,
                        help='The database path')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.database = os.path.abspath(os.path.expanduser(FLAGS.database))
    DEBUG = FLAGS.debug

    main()
