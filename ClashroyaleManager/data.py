import os
import json


class DataHandler(object):
    @staticmethod
    def load(path):
        if not os.path.exists(path):
            data = dict()
        else:
            with open(path, 'r') as f:
                data = json.load(f)
        return data

    @staticmethod
    def save(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=True, ensure_ascii=False)


data_handler = DataHandler()

