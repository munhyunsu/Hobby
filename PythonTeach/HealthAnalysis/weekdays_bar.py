import pickle

from matplotlib import pyplot as plt


def main():
    with open('bar_data/weeks.pickle', 'rb') as f:
        weeks, counts = pickle.load(f)

    print(weeks, counts)

    colors = ['ORANGERED', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'SLATEBLUE', 'ORANGE', (220/255, 118/255, 51/255)]
    plt.title('Steps by weekdays')
    plt.bar(weeks, counts, color=colors)
    plt.show()


if __name__ == '__main__':
    main()