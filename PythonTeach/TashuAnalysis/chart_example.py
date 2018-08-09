from matplotlib import pyplot as plt


def main_pie():
    x = ['A', 'B', 'C', 'D', 'E']
    y = [500, 200, 350, 100, 50]

    plt.pie(y, labels=x)
    plt.show()


if __name__ == '__main__':
    main_pie()