#!/usr/bin/env python3

import sys
import asyncio
import threading


class KWBServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        message = data.decode('utf-8')
        print('Received: {}'.format(message))
        self.transport.write(data)
        self.transport.close()

def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(KWBServerProtocol, 
                              '', 6292,
                              reuse_address = True,
                              reuse_port = True)
    print('서버 시작')
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('서버 종료')
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
