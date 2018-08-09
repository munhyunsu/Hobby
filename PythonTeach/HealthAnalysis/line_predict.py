from sklearn import linear_model
import pickle

from matplotlib import pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from HealthAnalysis.data_manager import DataManager


def main():
    data_manager = DataManager('google_data/')
    (feature, target) = data_manager.get_feature_data()

    # regr = linear_model.LinearRegression()
    regr = make_pipeline(PolynomialFeatures(5), Ridge())
    regr.fit(feature, target)

    with open('line_data/hours.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    for index in range(0, len(counts)):
        counts[index] = counts[index]//31

    plt.title('Hourly steps')
    plt.plot(hours, counts, 'mo--', label='Real (Average)')

    test_set = list()
    for index in range(0, 24):
        test_set.append([1, index])
    x = list(range(0, len(test_set)))
    y = regr.predict(test_set)
    plt.plot(x, y, label='Predict (5-Polynomial)')
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    plt.legend(loc=0)
    plt.show()


if __name__ == '__main__':
    main()