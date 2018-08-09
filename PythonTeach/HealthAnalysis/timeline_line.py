import pickle

from matplotlib import pyplot as plt


def main():
    with open('line_data/hours.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    print(hours, counts)

    plt.title('Hourly steps')
    plt.plot(hours, counts, 'mo--')
    plt.show()


if __name__ == '__main__':
    main()
