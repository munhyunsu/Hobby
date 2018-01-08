#!/usr/bin/env python3

import sys
import os
import json



def main(argv):
    """
    read all of files in directory inputed recursively.
    rename and copy(instead move for safety) file to specific rules.
    """
    os.makedirs('./outputs', exist_ok = True)

    dir_queue = argv[1:]
    file_queue = get_all_files(dir_queue)

    process_files(file_queue)



def process_files(file_queue):
    for target in file_queue:
        filename = target.split('/')[-1]
        user = filename.split('_')[0]
        user = 'A' + user[1:]
        date = filename.split('_')[1]
        data = (filename.split('_')[2]).split('.')[0]

        target_path = (data 
                     + '/' 
                     + date 
                     + '/' 
                     + user 
                     + '.json')
        target_path = './outputs/' + target_path

        os.makedirs('./outputs/' + data + '/' + date, exist_ok = True)
        with open(target, 'r') as read_filep:
            with open(target_path, 'w') as write_filep:
                read_json = json.load(read_filep)
                json.dump(read_json, write_filep,
                          indent = 4)

        print(target_path)





def get_all_files(dir_queue):
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
        


# is it good thing, right?
if __name__ == '__main__':
    sys.exit(main(sys.argv))
