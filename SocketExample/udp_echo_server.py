#!/usr/bin/env python3
# Echo server program (TCP)

import socket

HOST = ''
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(1024)
        print('Received by', addr, data)
        if not data: break
            
      
