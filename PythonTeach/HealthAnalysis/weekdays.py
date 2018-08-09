import os
import pickle

from HealthAnalysis.data_manager import DataManager


def main():
    data_manager = DataManager('data/')
    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = data_manager.get_weekday_steps()

    print('0 to 23: {0}'.format(counts))

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


if __name__ == '__main__':
    main()
