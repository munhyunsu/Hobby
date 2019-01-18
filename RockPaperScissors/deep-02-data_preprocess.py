import os
import csv
import time
import datetime
from collections import deque
import copy

RAWFILE = 'dummy.csv'
FIELDNAMES = ['unixtime', 'userid', 'hand', 'score']
TESTFILE = '/tmp/deep_rps.csv'
HISTORYLEN = 100
NAMERULE = 'b{0:04d}'
TESTFIELDNAMES = list()
HISTORYENTRY = dict()
for index in range(1, HISTORYLEN+1):
    name = NAMERULE.format(index)
    TESTFIELDNAMES.append('h_'+name)
    TESTFIELDNAMES.append('s_'+name)
    HISTORYENTRY['h_'+name] = 0
    HISTORYENTRY['s_'+name] = 0
TESTFIELDNAMES.append('hand')
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
    userid = int(row['userid'])
    hand = row['hand']
    score = row['score']
    history = HISTORY.get(userid, deque(maxlen=HISTORYLEN))
    data = {'hand': hand}
    data.update(get_history_one_hot(history))
    history.appendleft((hand, score))
    HISTORY[userid] = history
    return data


def get_history_one_hot(history):
    data = copy.deepcopy(HISTORYENTRY)
    for index in range(0, len(history)):
        name = NAMERULE.format(index+1)
        data['h_'+name] = history[index][0]
        data['s_'+name] = history[index][1]
    return data


if __name__ == '__main__':
    main()

