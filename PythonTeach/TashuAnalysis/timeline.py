import os
import csv
import datetime
from operator import itemgetter
import pickle


def main_2013_1():
    print('----- 2013 상반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2013_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['RENT_DATE'], '%Y%m%d%H%M%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2013_1.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_2013_2():
    print('----- 2013 하반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2013_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['RENT_DATE'], '%Y%m%d%H%M%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2013_2.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_2014_1():
    print('----- 2014 상반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2014_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y%m%d%H%M%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2014_1.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_2014_2():
    print('----- 2014 하반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2014_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y-%m-%d %H:%M:%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2014_2.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_2015_1():
    print('----- 2015 상반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2015_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'], '%Y-%m-%d %H:%M:%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2015_1.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_2015_2():
    print('----- 2015 하반기 시간별 대여수 -----')
    hour_count = dict()
    with open('data/2015_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['대여일시'][1:], '%Y%m%d%H%M%S')
                hour_count[date.hour] = hour_count.get(date.hour, 0) + 1
            except ValueError:
                pass

    hours = list(range(0, 24))
    counts = list()
    for hour in hours:
        if hour in hour_count:
            counts.append(hour_count[hour])
        else:
            counts.append(0)
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours_2015_2.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


if __name__ == '__main__':
    main_2013_1()
    main_2013_2()
    main_2014_1()
    main_2014_2()
    main_2015_1()
    main_2015_2()
