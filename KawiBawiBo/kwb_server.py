#!/usr/bin/env python3

import sys
import asyncio
import threading
import base64
import os

SRCPATH = './src/'

class KWBServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print('Connected: {}'.format(transport.get_extra_info('peername')))
        self.transport = transport
        self.method = None
        self.authorization = None
        self.content_length = None
        self.message = str()

    def data_received(self, data):
        transport = self.transport
        message = data.decode('utf-8')
        # 헤더 확인
        if self.method == None:
            self.method = message.split('\r\n')[0]
            if not self.method.startswith('POST / HTTP/1.1'):
                transport.write('400 Bad Request\r\n'.encode('ascii'))
                transport.close()
            # 헤더 파싱
            headers = message.split('\r\n\r\n')[0]
            for header in headers.split('\r\n'):
                if header.startswith('Authorization'):
                    self.authorization = header.split(' ')[-1]
                    self.authorization = \
                            base64.b64decode(self.authorization)
                    self.authorization = self.authorization.decode('utf-8')
                    print('Autorizing Info.: {}'.format(
                            self.authorization))
                elif header.startswith('Content-Length'):
                    self.content_length = int(header.split(' ')[-1])
                    if self.content_length > 10240:
                        transport.write(
                                '400 Bad Request\r\n'.encode('ascii'))
                        transport.close()
            if None in (self.method, 
                        self.authorization, 
                        self.content_length):
                transport.write('400 Bad Request\r\n'.encode('ascii'))
                transport.close()
            message = message.split('\r\n\r\n')[1:]
            message = ''.join(message)
        # 데이터 합치기
        self.message = self.message + message
        if self.content_length < len(self.message.encode('utf-8')):
            transport.write('400 Bad Request\r\n'.encode('ascii'))
            transport.close()
        if self.content_length == len(self.message.encode('utf-8')):
            if 'import random' in self.message:
                transport.write(
                        '400 Bad Request: import random\r\n'.encode(
                        'ascii'))
                transport.close()
            else:
                transport.write('202 Accepted\r\n'.encode('ascii'))
                transport.write(self.message.encode('utf-8'))
                filename = (SRCPATH 
                          + self.authorization.split(':')[0]
                          + '_'
                          + self.authorization.split(':')[1]
                          + '.py')
                with open(filename, 'w') as received_file:
                    received_file.write(self.message)
                transport.close()

    def eof_received(self):
        transport = self.transport
        self.transport.close()

    def connection_lost(self, exc):
        pass

def main():
    # 소스 디렉터리 생성
    os.makedirs(SRCPATH, exist_ok = True)
    loop = asyncio.get_event_loop()
    coro = loop.create_server(KWBServerProtocol, 
                              '', 6292,
                              reuse_address = True,
                              reuse_port = True)
    print('가위바위보 서버가 시작되었습니다.')
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('가위바위보 서버가 종료되었습니다.')
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
