import os
import csv
import time
import datetime

RAWFILE = 'dummy.csv'
FIELDNAMES = ['unixtime', 'userid', 'hand', 'score']
TESTFILE = '/tmp/deep_rps.csv'
TESTFIELDNAMES = ['month', 'weekday', 'hour', 'userid', 'prevhand',
                  'prevscore', 'hand']
HISTORY = dict()


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
    month = conv_time.tm_mon
    weekday = conv_time.tm_wday
    hour = conv_time.tm_hour
    userid = int(row['userid'])
    prevhand = HISTORY.get(userid, (0, 0))[0]
    prevscore = HISTORY.get(userid, (0, 0))[1]
    hand = row['hand']
    data = {'month': month,
            'weekday': weekday,
            'hour': hour,
            'userid': userid,
            'prevhand': prevhand,
            'prevscore': prevscore,
            'hand': hand}
    HISTORY[userid] = (row['hand'], row['score'])
    return data


if __name__ == '__main__':
    main()

