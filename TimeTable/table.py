import csv
from operator import itemgetter

class TimeTable(object):
    def __repr__(self):
        result = '|---+----+ 시간표 ----+----|\n'
        for node in self.table.keys():
            result = result + node + ': ' + self.table[node].__str__() + '\n'
        return result

    def __init__(self, path):
        self.path = path
        self.table = self.get_table_from_file()

    def get_table_from_file(self):
        result = dict()

        with open(self.path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                result[row['교사']] = [row['1'],
                                       row['2'],
                                       row['3'],
                                       row['4'],
                                       row['5'],
                                       row['6'],
                                       row['7']]

        return result

    def get_slot(self):
        slots = dict()
        table = self.table
        for key in table.keys():
            if (table[key][4] != '') and (table[key][5] != ''):
                slots[key] = table[key]

        return slots

    def get_target(self):
        targets = dict()
        table = self.table
        for key in table.keys():
            if (table[key][4] == '') and (table[key][5] == ''):
                targets[key] = table[key]

        return targets

    def find_by_room(self, room):
        result = list()
        table = self.table
        for key in table.keys():
            for index in range(0, len(table[key])):
                lecture = table[key][index]
                if lecture.endswith(room):
                    result.append((index, key, lecture))
        result.sort()
        return result
