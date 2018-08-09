import os
import csv
from operator import itemgetter
import pickle


def main_2013_1():
    print('----- 2013 상반기 Top 10 -----')
    rent_count = dict()
    with open('data/2013_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['RENT_STATION'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2013_1.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


def main_2013_2():
    print('----- 2013 하반기 Top 10 -----')
    rent_count = dict()
    with open('data/2013_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['RENT_STATION'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2013_2.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


def main_2014_1():
    print('----- 2014 상반기 Top 10 -----')
    rent_count = dict()
    with open('data/2014_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['대여 스테이션 정보'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2014_1.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


def main_2014_2():
    print('----- 2014 하반기 Top 10 -----')
    rent_count = dict()
    with open('data/2014_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['대여 스테이션 정보'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2014_2.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


def main_2015_1():
    print('----- 2015 상반기 Top 10 -----')
    rent_count = dict()
    with open('data/2015_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['대여 스테이션 정보'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2015_1.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


def main_2015_2():
    print('----- 2015 하반기 Top 10 -----')
    rent_count = dict()
    with open('data/2015_2.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                station = int(row['대여 스테이션 정보'])
            except ValueError:
                pass
            rent_count[station] = rent_count.get(station, 0) + 1

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    stations = list()
    counts = list()
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2015_2.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


if __name__ == '__main__':
    # main_2013_1()
    # main_2013_2()
    main_2014_1()
    # main_2014_2()
    # main_2015_1()
    # main_2015_2()