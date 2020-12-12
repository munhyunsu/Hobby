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


df1 = pd.read_csv('1.csv', header=1)
df1 = df1.fillna(0)
df1[df1.columns.values[3:]] = df1[df1.columns.values[3:]].astype('float16')
df1[df1.columns.values[3:]] = df1[df1.columns.values[3:]].round(2)
print(df1)

df2 = pd.read_csv('2.csv', header=1)
df2 = df2.fillna(0)
df2[df2.columns.values[3:]] = df2[df2.columns.values[3:]].astype('float16')
print(df2)

@app.route('/', methods=['GET'])
def score():
    num = request.args.get('num')
    if num is not None:
        num = int(num.strip())
    phone = request.args.get('phone')
    if phone is not None:
        phone = phone.strip()
    try:
        if (df1[df1['학번'] == num]['이메일'] == phone).values[0]:
            ss1 = df1[df1['학번'] == num]
            ss2 = df2[df2['학번'] == num]
        else:
            ss1 = ss2 = None
    except:
        ss1 = ss2 = None
        pass
    if ss1 is not None:
        print(f'{ss1 =}')
        print(f'{ss2 =}')
        return render_template('index.html', 
                               tables1=[ss1.to_html(index=False,
                                                    justify='center',
                                                    float_format='{:.2g}'.format)],
                               tables2=[ss2.to_html(index=False,
                                                    justify='center',
                                                    float_format='{:.2g}'.format)],)
    else:
        return render_template('index.html')

