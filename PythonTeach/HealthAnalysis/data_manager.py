import os
import csv
import re
import datetime


class DataManager(object):
    def __init__(self, path):
        self.path = path
        self.files = None

    def get_files(self, ext='.csv', recursive=True):
        if self.files is not None:
            return self.files
        path_list = [self.path]
        result = list()

        while len(path_list) > 0:
            cpath = path_list.pop()
            with os.scandir(cpath) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        if entry.name.endswith(ext):
                            result.append(entry.path)
                    else:
                        if recursive:
                            path_list.append(entry.path)

        self.files = result
        return self.files

    def get_hourly_steps(self):
        result_dict = dict()
        files = self.get_files()
        for file in files:
            step_list = self.get_steps(file)
            for (start_time, step) in step_list:
                date = self.get_time_struct(file, start_time, 9)
                result_dict[date.hour] = result_dict.get(date.hour, 0) + int(step)
        result = list()
        for index in range(0, 24):
            result.append(result_dict.get(index, 0))
        return result

    def get_steps(self, fpath):
        result = list()
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    start_time = row['Start time']
                    steps = int(row['Step count'])
                except ValueError:
                    continue
                result.append((start_time, steps))

        return result

    def get_time_struct(self, path, time_str, time_delta):
        # https://regexr.com/
        date_str = re.split(r'[/.]', path)[1] + ' ' + time_str[:8]
        date = datetime.datetime.strptime(date_str,
                                          '%Y-%m-%d %H:%M:%S')
        date = date + datetime.timedelta(hours=time_delta)
        date = date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=time_delta)))
        return date

    def get_weekday_steps(self):
        weeks = {0: 'Mon',
                 1: 'Tue',
                 2: 'Wed',
                 3: 'Thu',
                 4: 'Fri',
                 5: 'Sat',
                 6: 'Sun'}
        result_dict = dict()
        files = self.get_files()
        for file in files:
            step_list = self.get_steps(file)
            for (start_time, step) in step_list:
                date = self.get_time_struct(file, start_time, 9)
                result_dict[weeks[date.weekday()]] = result_dict.get(weeks[date.weekday()], 0) + int(step)

        weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        counts = list()
        for week in weeks:
            counts.append(result_dict[week])
        return counts

    def get_feature_data(self):
        feature_vector = list()
        target_vector = list()
        files = self.get_files()
        for file in files:
            step_list = self.get_steps(file)
            for (start_time, step) in step_list:
                date = self.get_time_struct(file, start_time, 9)
                # feature_vector.append([date.year, date.month, date.day, date.weekday(), date.hour])
                feature_vector.append([date.weekday(), date.hour])
                target_vector.append([step])

        return feature_vector, target_vector
