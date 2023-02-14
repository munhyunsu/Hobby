import os
import asyncio
import pprint

import simpleobsws

import secret

FLAGS = _ = None
DEBUG = False


async def amain():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    ws = simpleobsws.WebSocketClient(url=f'ws://{secret.ip}:{secret.port}',
                                     password=f'{secret.password}')

    await ws.connect()
    await ws.wait_until_identified()

    request = simpleobsws.Request(FLAGS.job)

    ret = await ws.call(request)
    if ret.ok():
        pprint.pprint(ret.responseData)

    await ws.disconnect()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--job', required=True,
                        help='The job via websocket')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    asyncio.run(amain())
