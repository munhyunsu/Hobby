import os
import csv
import time
import datetime

RAWFILE = 'dummy.csv'
FIELDNAMES = ['unixtime', 'userid', 'hand', 'score']
TESTFILE = '/tmp/deep_rps.csv'
TESTFIELDNAMES = ['month', 'weekday', 'hour', 'winrate', 'drawrate',
                  'loserate', 'prevhand', 'prevscore', 'hand']
TESTFIELDNAMES = ['month_1', 'month_2', 'month_3', 'month_4', 'month_5',
                  'month_6', 'month_7', 'month_8', 'month_9', 'month_10',
                  'month_11', 'month_12',
                  'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
                  'weekday_4', 'weekday_5', 'weekday_6',
                  'hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4',
                  'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                  'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14',
                  'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19',
                  'hour_20', 'hour_21', 'hour_22', 'hour_23',
                  'winrate', 'drawrate', 'loserate', 
                  'prevhand_0', 'prevhand_1', 'prevhand_2', 'prevhand_3',
                  'prevscore_0', 'prevscore_1', 'prevscore_2', 'prevscore_3',
                  'hand']
HISTORY = dict()
RESULT = dict()

def main():
    if not os.path.exists(RAWFILE):
        return False
    with open(TESTFILE, 'w') as file_out:
        writer = csv.DictWriter(file_out, fieldnames=TESTFIELDNAMES)
        writer.writeheader()
        with open(RAWFILE, 'r') as file_in:
            reader = csv.DictReader(file_in)
            for row in reader:
                data = form_data(row)
                writer.writerow(data)

def form_data(row):
    """Data
    weekday: 0: Monday 6: Sunday
    prevhand: {0: None, 1: Rock, 2: Paper, 3: Scissors}
    prevscore: {0: None, 1: Win, 2: Draw, 3: Lose}
    """
    global HISTORY
    conv_time = time.localtime(int(float(row['unixtime'])))
    month = int(conv_time.tm_mon)
    weekday = int(conv_time.tm_wday)
    hour = int(conv_time.tm_hour)
    userid = int(row['userid'])
    result = RESULT.get(userid, [0, 0, 0])
    if row['score'] == '1':
        result[0] = result[0] + 1
    elif row['score'] == '2':
        result[1] = result[1] + 1
    elif row['score'] == '3':
        result[2] = result[2] + 1
    winrate = int(result[0])
    drawrate = int(result[1])
    loserate = int(result[2])
    prevhand = int(HISTORY.get(userid, (0, 0))[0])
    prevscore = int(HISTORY.get(userid, (0, 0))[1])
    hand = row['hand']
    #data = {'month': month/12,
    #        'weekday': weekday/6,
    #        'hour': hour/23,
    #        'winrate': winrate/sum(result),
    #        'drawrate': drawrate/sum(result),
    #        'loserate': loserate/sum(result),
    #        'prevhand': prevhand/3,
    #        'prevscore': prevscore/3,
    #        'hand': hand}
    data = {'winrate': winrate/sum(result),
            'drawrate': drawrate/sum(result),
            'loserate': loserate/sum(result),
            'hand': hand}
    data.update(get_one_hot(month, 'month_', 1, 12))
    data.update(get_one_hot(weekday, 'weekday_', 0, 6))
    data.update(get_one_hot(hour, 'hour_', 0, 23))
    data.update(get_one_hot(prevhand, 'prevhand_', 0, 3))
    data.update(get_one_hot(prevscore, 'prevscore_', 0, 3))
    HISTORY[userid] = (row['hand'], row['score'])
    RESULT[userid] = result
    return data


def get_one_hot(data, prefix, minimum, maximum):
    result = dict()
    for index in range(minimum, maximum+1):
        result['{0}{1}'.format(prefix, index)] = 0
    result['{0}{1}'.format(prefix, data)] = 1
    return result


if __name__ == '__main__':
    main()

