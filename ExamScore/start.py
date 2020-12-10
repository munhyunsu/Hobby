import os
import pandas as pd

from flask import Flask, request, render_template, redirect


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


df = pd.read_csv('score.csv')
df = df.fillna(0)
df[df.columns.values[3:]] = df[df.columns.values[3:]].astype('float16')
#print(df)

@app.route('/', methods=['GET'])
def score():
    num = request.args.get('num')
    if num is not None:
        num = int(num.strip())
    phone = request.args.get('phone')
    if phone is not None:
        phone = phone.strip()
    try:
        if (df[df['학번'] == num]['이메일'] == phone).values[0]:
            ss = df[df['학번'] == num]
        else:
            ss = None
    except:
        ss = None
        pass
    if ss is not None:
        print(f'{ss}')
        return render_template('index.html', 
                               tables=[ss.to_html(index=False,
                                                  justify='center')],)
    else:
        return render_template('index.html')

