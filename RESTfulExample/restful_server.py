import sys
import socketserver

from rest_handler import RESTRequestHandler
from server_daemon import HTTPDaemon


IPADDRESS = ''
PORT = 8080
HANDLER = RESTRequestHandler


def main():
    #with socketserver.TCPServer((IPADDRESS, PORT), HANDLER) as httpd:
    with HTTPDaemon((IPADDRESS, PORT), HANDLER) as httpd:
        print('serving at port', PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
