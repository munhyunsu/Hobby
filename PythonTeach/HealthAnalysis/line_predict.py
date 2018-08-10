from sklearn import linear_model
import sys
import pickle

from matplotlib import pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from HealthAnalysis.data_manager_google import DataManagerGoogle
from HealthAnalysis.data_manager_apple import DataManagerApple
from HealthAnalysis.data_manager_samsung import DataManagerSamsung


def get_feature_data(steps):
    feature_vector = list()
    target_vector = list()
    for time_struct, step in steps:
        feature_vector.append([time_struct.weekday(), time_struct.hour])
        target_vector.append([step])

    return feature_vector, target_vector


def main(argv=()):
    if len(argv) < 2:
        sys.exit(0)
    if argv[1] == 'google':
        data_manager = DataManagerGoogle('google_data/')
    elif argv[1] == 'apple':
        data_manager = DataManagerApple('apple_data/')
    elif argv[1] == 'samsung':
        data_manager = DataManagerSamsung('samsung_data/')
    else:
        sys.exit(0)
    step_list = data_manager.get_steps()
    (feature, target) = get_feature_data(step_list)


    # regr = linear_model.LinearRegression()
    regr = make_pipeline(PolynomialFeatures(10), Ridge())
    regr.fit(feature, target)

    with open('line_data/hours.pickle', 'rb') as f:
        hours, counts = pickle.load(f)

    for index in range(0, len(counts)):
        counts[index] = counts[index]//240

    plt.title('Hourly steps')
    plt.plot(hours, counts, 'mo--', label='Real (Average)')

    test_set = list()
    for index in range(0, 24):
        test_set.append([1, index])
    x = list(range(0, len(test_set)))
    y = regr.predict(test_set)
    plt.plot(x, y, label='Predict (10-Polynomial)')
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    plt.legend(loc=0)
    plt.show()


if __name__ == '__main__':
    # main(('line_predict.py', 'google'))
    # main(('line_predict.py', 'apple'))
    main(('line_predict.py', 'samsung'))