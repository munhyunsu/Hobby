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
    print('----- 2013 상반기 요일별 대여수 -----')
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


def main_2013_2():
    print('----- 2013 하반기 요일별 대여수 -----')
    weekday_count = dict()
    with open('data/2013_2.csv', 'r') as f:
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
    with open('bar_data/weeks_2013_2.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_2014_1():
    print('----- 2014 상반기 요일별 대여수 -----')
    weekday_count = dict()
    with open('data/2014_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y%m%d%H%M%S')
                weekday_count[WEEKS[date.weekday()]] = weekday_count.get(WEEKS[date.weekday()], 0) + 1
            except ValueError:
                pass

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        print('{0}: {1}'.format(week, weekday_count[week]))
        counts.append(weekday_count[week])

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks_2014_1.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_2014_2():
    print('----- 2014 하반기 요일별 대여수 -----')
    weekday_count = dict()
    with open('data/2014_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y-%m-%d %H:%M:%S')
                weekday_count[WEEKS[date.weekday()]] = weekday_count.get(WEEKS[date.weekday()], 0) + 1
            except ValueError:
                pass

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        print('{0}: {1}'.format(week, weekday_count[week]))
        counts.append(weekday_count[week])

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks_2014_2.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_2015_1():
    print('----- 2015 상반기 요일별 대여수 -----')
    weekday_count = dict()
    with open('data/2015_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y-%m-%d %H:%M:%S')
                weekday_count[WEEKS[date.weekday()]] = weekday_count.get(WEEKS[date.weekday()], 0) + 1
            except ValueError:
                pass

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        print('{0}: {1}'.format(week, weekday_count[week]))
        counts.append(weekday_count[week])

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks_2015_1.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_2015_2():
    print('----- 2015 하반기 요일별 대여수 -----')
    weekday_count = dict()
    with open('data/2015_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'][1:], '%Y%m%d%H%M%S')
                weekday_count[WEEKS[date.weekday()]] = weekday_count.get(WEEKS[date.weekday()], 0) + 1
            except ValueError:
                pass

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        print('{0}: {1}'.format(week, weekday_count[week]))
        counts.append(weekday_count[week])

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks_2015_2.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


if __name__ == '__main__':
    main_2013_1()
    main_2013_2()
    main_2014_1()
    main_2014_2()
    main_2015_1()
    main_2015_2()
