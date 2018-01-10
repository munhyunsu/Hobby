#!/usr/bin/env python3

import sys
import os
import logging
import json

FORMAT = '%(created)s:%(levelno)s:%(message)s'
logging.basicConfig(stream = sys.stdout,
                    format = FORMAT,
                    level = logging.DEBUG)

def main(argv):
    if len(argv) < 2:
        logging.debug('We need argument for path')
        return

    file_queue = get_file_list(argv[1:])
    print(get_data_from_list(file_queue))




def get_file_list(dir_queue):
    file_queue = list()

    while len(dir_queue) > 0:
        path = dir_queue.pop()
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    file_queue.append(entry.path)
                else:
                    dir_queue.append(entry.path)

    return file_queue



def get_data_from_list(file_queue):
    while len(file_queue) > 0:
        path = file_queue.pop()
        with open(path, 'r') as rfile:
            data = json.load(rfile)
            return data



# is it good thing, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
