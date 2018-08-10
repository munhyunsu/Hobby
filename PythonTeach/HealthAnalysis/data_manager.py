import os
import csv
import re
import datetime


class DataManager(object):
    def __init__(self, path, ext=''):
        self.path = path
        self.ext = ext
        self.files = None

    def get_files(self, recursive=True):
        if self.files is not None:
            return self.files
        path_list = [self.path]
        result = list()

        while len(path_list) > 0:
            cpath = path_list.pop()
            with os.scandir(cpath) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        if entry.name.endswith(self.ext):
                            result.append(entry.path)
                    else:
                        if recursive:
                            path_list.append(entry.path)

        self.files = result
        return self.files

    def get_steps(self):
        steps = list()
        files = self.get_files()
        for file in files:
            parsed_list = self.parse_file(file)
            for (time_struct, step) in parsed_list:
                steps.append((time_struct, step))
        return steps

    def parse_file(self, fpath):
        raise NotImplementedError


def main():
    dm = DataManager('google_data')
    print(dm.get_steps())


if __name__ == '__main__':
    main()