import os
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


def main():
    for fname in get_files('./', ext='webp'):
        oname = fname[:-4] + 'png'
        fname = fname.replace(' ', '\ ')
        oname = oname.replace(' ', '\ ')
        command = './dwebp {0} -o {1}'.format(fname, oname)
        print(command)
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    main()
