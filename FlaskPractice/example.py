#!/usr/bin/env python3

from flask import Flask

app =  Flask(__name__)

@app.route('/')
def hello():
    with open('target.txt', 'r') as f:
        return f.read()


@app.route('/cho')
def hello_cho():
    return 'cho!!'

app.run(debug = True)
