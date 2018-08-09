import os
import pickle

from HealthAnalysis.data_manager_google import DataManagerGoogle
from HealthAnalysis.data_manager_apple import DataManagerApple
from HealthAnalysis.data_manager_samsung import DataManagerSamsung


def get_weekday_steps(steps):
    weeks = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu',
             4: 'Fri', 5: 'Sat', 6: 'Sun'}
    result_dict = dict()
    for time_struct, step in steps:
        result_dict[weeks[time_struct.weekday()]] = result_dict.get(weeks[time_struct.weekday()], 0) + int(step)

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    counts = list()
    for week in weeks:
        counts.append(result_dict[week])
    return counts


def main_google():
    data_manager = DataManagerGoogle('google_data/')
    step_list = data_manager.get_steps()
    counts = get_weekday_steps(step_list)

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    print('0 to 23: {0}'.format(counts))

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_apple():
    data_manager = DataManagerApple('apple_data/')
    step_list = data_manager.get_steps()
    counts = get_weekday_steps(step_list)

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    print('0 to 23: {0}'.format(counts))

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


def main_samsung():
    data_manager = DataManagerSamsung('samsung_data/')
    step_list = data_manager.get_steps()
    counts = get_weekday_steps(step_list)

    weeks = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    print('0 to 23: {0}'.format(counts))

    os.makedirs('bar_data', exist_ok=True)
    with open('bar_data/weeks.pickle', 'wb') as f:
        pickle.dump((weeks, counts), f)


if __name__ == '__main__':
    # main_google()
    # main_apple()
    main_samsung()