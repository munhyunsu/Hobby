#!/usr/bin/env python3
# Echo client program (TCP)

import socket

HOST = ''
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b'Hello, world', (HOST, PORT))
