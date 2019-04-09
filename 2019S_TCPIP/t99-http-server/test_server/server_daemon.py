from socketserver import TCPServer


class HTTPDaemon(TCPServer):
    allow_reuse_address = True
