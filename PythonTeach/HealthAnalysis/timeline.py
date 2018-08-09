import os
import pickle

from HealthAnalysis.data_manager_google import DataManagerGoogle
from HealthAnalysis.data_manager_apple import DataManagerApple
from HealthAnalysis.data_manager_samsung import DataManagerSamsung


def get_hourly_steps(steps):
    result_dict = dict()
    for time_struct, step in steps:
        result_dict[time_struct.hour] = result_dict.get(time_struct.hour, 0) + int(step)

    result = list()
    for index in range(0, 24):
        result.append(result_dict.get(index, 0))
    return result


def main_google():
    data_manager = DataManagerGoogle('google_data/')
    step_list = data_manager.get_steps()
    counts = get_hourly_steps(step_list)

    hours = list(range(0, 24))
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_apple():
    data_manager = DataManagerApple('apple_data/')
    step_list = data_manager.get_steps()
    counts = get_hourly_steps(step_list)

    hours = list(range(0, 24))
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


def main_samsung():
    data_manager = DataManagerSamsung('samsung_data/')
    step_list = data_manager.get_steps()
    counts = get_hourly_steps(step_list)

    hours = list(range(0, 24))
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


if __name__ == '__main__':
    main_google()
    # main_apple()
    # main_samsung()