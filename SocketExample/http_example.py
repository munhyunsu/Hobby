#!/usr/bin/env python3
# Echo client program (TCP)

import socket

HOST = ''
PORT = 80
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'GET / HTTP/1.1\r\n\r\n')
    data = s.recv(1024)
print('Received', repr(data))
