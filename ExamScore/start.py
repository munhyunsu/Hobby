from flask import Flask, request, render_template, redirect
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def checkin():
    if request.method == 'GET':
        student = request.args.get('id')
        history = list()
        if student is not None:
            history = get_history(student)
        return render_template('index.html', histories=history)
    elif request.method == 'POST':
        headers = request.headers
        data = request.get_json()

        if data['password'] == 'abcd':
            print('Pass', data['student'])

        return redirect(f'/?id={data["student"]}', code=302)
        
    
