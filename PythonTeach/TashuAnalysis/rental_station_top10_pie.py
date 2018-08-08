import pickle

from matplotlib import pyplot as plt


def main_2013_1():
    with open('pie_data/top10_2013_1.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2013 SS, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    # plt.savefig('pie_2013_1.png')
    plt.show()


def main_2013_2():
    with open('pie_data/top10_2013_2.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2013 FW, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    plt.show()


def main_2014_1():
    with open('pie_data/top10_2014_1.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2014 SS, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    plt.show()


def main_2014_2():
    with open('pie_data/top10_2014_2.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2014 FW, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    plt.show()


def main_2015_1():
    with open('pie_data/top10_2015_1.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2015 SS, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    plt.show()


def main_2015_2():
    with open('pie_data/top10_2015_2.pickle', 'rb') as f:
        stations, counts = pickle.load(f)

    plt.title('2015 FW, Tashu Top 10 Ratio')
    plt.pie(counts, labels=stations)
    plt.show()


if __name__ == '__main__':
    main_2013_1()
    main_2013_2()
    main_2014_1()
    main_2014_2()
    main_2015_1()
    main_2015_2()