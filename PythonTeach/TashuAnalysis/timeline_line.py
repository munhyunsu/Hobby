import pickle

from matplotlib import pyplot as plt


def main_2013_1():
    with open('line_data/hours_2013_1.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    # color: https://htmlcolorcodes.com/
    # format string: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    plt.title('Rent counts timeline, 2013 SS')
    plt.axis([0, 23, 0, 40000])
    # plt.plot(hours, counts, '#7D32A1')
    plt.plot(hours, counts, 'g.-')
    plt.show()


def main_2013_2():
    with open('line_data/hours_2013_2.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Rent counts timeline, 2013 FW')
    plt.plot(hours, counts, 'b-.')
    plt.show()


def main_2014_1():
    with open('line_data/hours_2014_1.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Rent counts timeline, 2014 SS')
    plt.plot(hours, counts, 'r,:')
    plt.show()


def main_2014_2():
    with open('line_data/hours_2014_2.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Rent counts timeline, 2014 FW')
    plt.plot(hours, counts, 'c+-')
    plt.show()


def main_2015_1():
    with open('line_data/hours_2015_1.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Rent counts timeline, 2015 SS')
    plt.plot(hours, counts, 'k--')
    plt.show()


def main_2015_2():
    with open('line_data/hours_2015_2.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Rent counts timeline, 2015 FW')
    plt.plot(hours, counts, 'mo-')
    plt.show()


if __name__ == '__main__':
    main_2013_1()
    main_2013_2()
    main_2014_1()
    main_2014_2()
    main_2015_1()
    main_2015_2()
