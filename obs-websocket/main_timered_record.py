import os
import asyncio
import pprint
import json
import subprocess
import shlex

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

    request = simpleobsws.Request('StartRecord')
    ret = await ws.call(request)
    if ret.ok():
        pprint.pprint(ret.responseData)

    await asyncio.sleep(FLAGS.minutes*60)

    request = simpleobsws.Request('StopRecord')
    ret = await ws.call(request)
    if ret.ok():
        pprint.pprint(ret.responseData)

    await asyncio.sleep(int(FLAGS.minutes*60*0.1))

    if FLAGS.audio_only:
        ipath = ret.responseData['outputPath']
        opath = f'{os.path.splitext(ipath)[0]}.mp3'
        command = shlex.split(f'ffmpeg -i "{ipath}" -c:a libmp3lame "{opath}"')
        if DEBUG:
            print(f'Run: {command}')
        subprocess.run(command)

    await ws.disconnect()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--minutes', required=True, type=int,
                        help='The recording minutes')
    parser.add_argument('--audio_only', action='store_true',
                        help='The audio only recoding')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    asyncio.run(amain())
