import os
import sys
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
    counts = get_hourly_steps(step_list)

    hours = list(range(0, 24))
    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


if __name__ == '__main__':
    # main(('timeline.py', 'google'))
    # main(('timeline.py', 'apple'))
    main(('timeline.py', 'samsung'))