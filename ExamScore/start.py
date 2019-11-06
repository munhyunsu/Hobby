import os
import csv

from flask import Flask, request, render_template, redirect

RESULT = os.path.abspath(os.path.expanduser('./midresult.csv'))

def stoi(l):
    result = list()
    for e in l:
        try:
            result.append(int(e))
        except:
            result.append(0)
    return result

app = Flask(__name__)
data = dict()


with open(RESULT, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        num = row[0]
        name = row[1]
        s1 = stoi(row[2:12])
        s2 = stoi(row[12:18])
        s3 = stoi(row[18:21])
        s4 = stoi(row[21:25])
        s5 = stoi(row[25:29])
        print(f'Loaded: {num} {name}')
        data[(num, name)] = (s1, s2, s3, s4, s5)


@app.route('/', methods=['GET'])
def score():
    num = request.args.get('num')
    if num is not None:
        num = num.strip()
    name = request.args.get('name')
    if name is not None:
        name = name.strip()
    score = data.get((num, name), None)
    if score is not None:
        tscore = list()
        for s in score:
            tscore.append(sum(s))
        total = sum(tscore)
        print(f'{num} {name} {score}')
        return render_template('index.html', num=num,
                                             name=name,
                                             score=score,
                                             tscore=tscore,
                                             total=total,
                                             length=len(score))
    else:
        return render_template('index.html')

