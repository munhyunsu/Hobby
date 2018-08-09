import csv
import datetime
import re

from HealthAnalysis.data_manager import DataManager


class DataManagerGoogle(DataManager):
    def __init__(self, path, ext=''):
        super().__init__(path, ext)

    def parse_file(self, fpath):
        result = list()
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    time_struct = self.get_time_struct(fpath, row['Start time'], 9)
                    steps = int(row['Step count'])
                except ValueError:
                    continue
                result.append((time_struct, steps))

        return result

    def get_time_struct(self, path, time_str, time_delta):
        # https://regexr.com/
        date_str = re.split(r'[/.]', path)[1] + ' ' + time_str[:8]
        date = datetime.datetime.strptime(date_str,
                                          '%Y-%m-%d %H:%M:%S')
        date = date + datetime.timedelta(hours=time_delta)
        date = date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=time_delta)))
        return date


def main():
    dm = DataManagerGoogle('google_data', '.csv')
    print(dm.get_steps())


if __name__ == '__main__':
    main()