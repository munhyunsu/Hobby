import os
import pickle

from HealthAnalysis.data_manager import DataManager


def main():
    data_manager = DataManager('data/')
    hours = list(range(0, 24))
    counts = data_manager.get_hourly_steps()

    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


if __name__ == '__main__':
    main()
