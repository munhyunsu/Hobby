import csv
import json
import datetime

from HealthAnalysis.data_manager import DataManager


class DataManagerSamsung(DataManager):
    def __init__(self, path, ext=''):
        super().__init__(path, ext)

    def parse_file(self, fpath):
        result = list()
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['source_type']) != 0:
                    continue
                json_record = self.parse_json(int(row['day_time'])//1000,
                                              'samsung_data/jsons/'+ row['binning_data'],
                                              9)
                result.extend(json_record)

        return result

    def parse_json(self, unixtime, json_path, time_delta):
        result = list()
        time_pointer = datetime.datetime.fromtimestamp(unixtime,
                                                       tz=datetime.timezone(datetime.timedelta(hours=time_delta)))
        # BUG?
        time_pointer = time_pointer - datetime.timedelta(hours=time_delta)
        with open(json_path, 'r') as f:
            json_data = json.load(f)
            for entry in json_data:
                step = int(entry['count'])
                if step != 0:
                    result.append((time_pointer, step))
                time_pointer = time_pointer + datetime.timedelta(minutes=10)

        return result


def main():
    dm = DataManagerSamsung('samsung_data', '.csv')
    print(dm.get_steps())


if __name__ == '__main__':
    main()