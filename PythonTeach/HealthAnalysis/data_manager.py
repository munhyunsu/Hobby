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





    #
    # def get_steps(self, fpath):
    #     result = list()
    #     with open(fpath, 'r') as f:
    #         reader = csv.DictReader(f)
    #         for row in reader:
    #             try:
    #                 start_time = row['Start time']
    #                 steps = int(row['Step count'])
    #             except ValueError:
    #                 continue
    #             result.append((start_time, steps))
    #
    #     return result

    # def get_time_struct(self, path, time_str, time_delta):
    #     # https://regexr.com/
    #     date_str = re.split(r'[/.]', path)[1] + ' ' + time_str[:8]
    #     date = datetime.datetime.strptime(date_str,
    #                                       '%Y-%m-%d %H:%M:%S')
    #     date = date + datetime.timedelta(hours=time_delta)
    #     date = date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=time_delta)))
    #     return date
    #

    #
    # def get_feature_data(self):
    #     feature_vector = list()
    #     target_vector = list()
    #     files = self.get_files(ext='.csv')
    #     for file in files:
    #         step_list = self.get_steps(file)
    #         for (start_time, step) in step_list:
    #             date = self.get_time_struct(file, start_time, 9)
    #             # feature_vector.append([date.year, date.month, date.day, date.weekday(), date.hour])
    #             feature_vector.append([date.weekday(), date.hour])
    #             target_vector.append([step])
    #
    #     return feature_vector, target_vector


def main():
    dm = DataManager('google_data')
    print(dm.get_steps())


if __name__ == '__main__':
    main()