#!/usr/bin/env python3

import sys
import asyncio
import time


import asyncio


async def task_func():
    print('in task_func')
    msg = input('input: ')
    #return 'the result'
    return msg


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    print('waiting for {!r}'.format(task))
    return_value = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(return_value))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
