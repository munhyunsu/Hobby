import datetime
import xml.etree.ElementTree as ET

from HealthAnalysis.data_manager import DataManager


class DataManagerApple(DataManager):
    def __init__(self, path, ext=''):
        super().__init__(path, ext)

    def parse_file(self, fpath):
        result = list()
        tree = ET.parse(fpath)
        root = tree.getroot()
        for record in root[2:]:
            record_attrib = record.attrib
            if record_attrib['type'] != 'HKQuantityTypeIdentifierStepCount':
                continue
            time_struct = self.get_time_struct(record_attrib['startDate'])
            steps = int(record_attrib['value'])
            result.append((time_struct, steps))

        return result

    def get_time_struct(self, time_str):
        date = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S %z')
        return date


def main():
    dm = DataManagerApple('apple_data', '.xml')
    print(dm.get_steps())


if __name__ == '__main__':
    main()