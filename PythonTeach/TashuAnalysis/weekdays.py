import os
import csv
import datetime
from operator import itemgetter
import pickle

WEEKS = {0: 'Mon',
         1: 'Tue',
         2: 'Wed',
         3: 'Thu',
         4: 'Fri',
         5: 'Sat',
         6: 'Sun'}


def main_2013_1():
    print('----- 2013 상반기 Top 10 -----')
    weekday_count = dict()
    with open('data/2013_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['RENT_DATE'], '%Y%m%d%H%M%S')
                weekday_count[WEEKS[date.weekday()]] = weekday_count.get(WEEKS[date.weekday()], 0) + 1
            except ValueError:
                pass

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        print('{0}: {1}'.format(week, weekday_count[week]))
        counts.append(weekday_count[week])

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks_2013_1.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


if __name__ == '__main__':
    main_2013_1()