import os
import csv
import pickle

from operator import itemgetter

from matplotlib import pyplot as plt


def main_2013_1():
    rent_count = dict()
    with open('processed_data/station_count_2013_1.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rent_count[row['station']] = int(row['count'])

    rent_list = list()
    for key in rent_count.keys():
        rent_list.append((key, rent_count[key]))

    rent_list = sorted(rent_list, key=itemgetter(1), reverse=True)
    for index in range(0, 10):
        print('Station: {0}, Count: {1}'.format(rent_list[index][0], rent_list[index][1]))

    stations = list()
    counts = list()
    for index in range(0, 10):
        stations.append(rent_list[index][0])
        counts.append(rent_list[index][1])

    plt.pie(counts, labels=stations)
    plt.show()

    os.makedirs('pie_data', exist_ok=True)
    with open('pie_data/top10_2013_1.pickle', 'wb') as f:
        pickle.dump((stations, counts), f)


if __name__ == '__main__':
    main_2013_1()