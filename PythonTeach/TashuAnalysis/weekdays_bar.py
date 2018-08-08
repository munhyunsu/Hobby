import pickle

from matplotlib import pyplot as plt


def main_2013_1():
    with open('bar_data/weeks_2013_1.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2013 SS')
    plt.bar(weeks, counts, color=colors)
    plt.show()


def main_2013_2():
    with open('bar_data/weeks_2013_2.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2013 FW')
    plt.bar(weeks, counts, color=colors)
    plt.show()


def main_2014_1():
    with open('bar_data/weeks_2014_1.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2014 SS')
    plt.bar(weeks, counts, color=colors)
    plt.show()


def main_2014_2():
    with open('bar_data/weeks_2014_2.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2014 FW')
    plt.bar(weeks, counts, color=colors)
    plt.show()


def main_2015_1():
    with open('bar_data/weeks_2015_1.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2015 SS')
    plt.bar(weeks, counts, color=colors)
    plt.show()


def main_2015_2():
    with open('bar_data/weeks_2015_2.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    # Color maps(HTML color): https://htmlcolorcodes.com/color-names/
    # RGB or RGBA [0, 1]
    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Rent counts by weekdays, 2015 FW')
    plt.bar(weeks, counts, color=colors)
    plt.show()


if __name__ == '__main__':
    main_2013_1()
    # main_2013_2()
    # main_2014_1()
    # main_2014_2()
    # main_2015_1()
    # main_2015_2()
