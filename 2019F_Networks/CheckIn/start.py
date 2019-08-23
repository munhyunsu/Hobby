import asyncio


FLAGS = None


async def client_handler(reader, writer):
    print(f'Connected with {writer.get_extra_info("peername")}')
    cdata = (await reader.read(1500)).decode('utf-8')
    try:
        cmethod, cpath, cproto = (cdata.split('\r\n')[0]).split(' ')
    except:
        writer.close()

    if cmethod == 'GET':
        sdata = ('HTTP/1.1 200 OK\r\n'
                 'Content-Type: text/html; encoding=utf8\r\n'
                 'Content-Length: 6\r\n'
                 'Connection: close\r\n'
                 '\r\n'
                 'GET OK').encode('utf-8')
    elif cmethod == 'POST':
        sdata = ('HTTP/1.1 200 OK\r\n'
                 'Content-Type: text/html; encoding=utf8\r\n'
                 'Content-Length: 7\r\n'
                 'Connection: close\r\n'
                 '\r\n'
                 'POST OK').encode('utf-8')
    writer.write(sdata)
    await writer.drain()
    writer.close()


def main(_):
    print(f'Parsed args {FLAGS}')
    print(f'Unparsed args {_}')

    # get event loop
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(client_handler,
                                '', FLAGS.port,
                                loop=loop,
                                reuse_address=True)
    server = loop.run_until_complete(coro)

    print('Start Server')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('End Server')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8888,
                        help='Server port number')

    FLAGS, _ = parser.parse_known_args()

    main(_)

