import sys
import os
from operator import itemgetter
import shutil
import subprocess

def get_files(path, ext = '', recursive = False):
    '''
    Read all files in path
    :param path: path for reading
    :return: absolute path of all files in directory list
    '''
    path_list = [path]

    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        yield entry.path
                    else:
                        if recursive == True:
                            path_list.append(entry.path)



def get_files_by_mtime(path):
    result = list()

    for fpath in get_files(path):
        mtime = os.stat(fpath).st_mtime_ns
        result.append((fpath, mtime))

    result.sort(key = itemgetter(1))

    return result



def move_copied_file(path):
    command = 'mv path ./original'
    subprocess.check_call(command, shell=True)
    command = 'mv ./output path'
    subprocess.check_call(command, shell=True)

    return True




def copy_files(path_list, prefix):
    os.makedirs('./output', exist_ok = True)
    for index in range(0, len(path_list)):
        spath = path_list[index][0]
        opath = './output/{0}{1:03d}.{2}'.format(prefix, index+1, spath.split('.')[-1])
        shutil.copy2(spath, opath)
        # print('{0} to {1}'.format(spath, opath))

    return index+1