import os
import csv

from flask import Flask, request, render_template, redirect

RESULT = os.path.abspath(os.path.expanduser('./Final2.csv'))

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
        score = int(row[2])
        print(f'Loaded: {num} {name}')
        data[(num, name)] = score


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
        #print(f'{num} {name} {score}')
        return render_template('index_netx.html', num=num,
                                                  name=name,
                                                  score=score,
                                                  )
    else:
        return render_template('index_netx.html')

