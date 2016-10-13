#!/usr/bin/python3

import os
import sys
import subprocess


def _unzip_cp949(input_path):
    print('Unzip', input_path)
    unzipdir = input_path[:-4]
    p = subprocess.Popen(['unzip', '-O', 'CP949', '-d', unzipdir, \
            input_path], stdout = subprocess.PIPE)
    p.wait()



def unzip_cp949(input_path):
    dirfiles = os.listdir(path = input_path)
    unzip_queue = list()
    for new_file in dirfiles:
        unzip_queue.append(input_path + '/' + new_file)
    
    while len(unzip_queue) > 0:
        files = unzip_queue.pop()
        if os.path.isdir(files):
            dirfiles = os.listdir(path = files)
            for new_file in dirfiles:
                unzip_queue.append(files + '/' + new_file)
            continue
        if files[-3:] == 'zip':
            _unzip_cp949(files)
        else:
            print('Not zip', files)



def main():
    if len(sys.argv) > 2:
        print('We need input path')
        sys.exit()

    input_path = os.path.abspath(sys.argv[1])

    unzip_cp949(input_path)



if __name__ == '__main__':
    main()
