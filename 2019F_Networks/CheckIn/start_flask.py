from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse


def get_history(student):
    return [4, 3, 2, 1]


class CheckIn(Resource):
    def get(self):
        student = request.args.get('id')
        history = list()
        if student is not None:
            history = get_history(student)
        return {'History': history}


    def post(self):
        headers = request.headers
        data = request.get_json()

        if data['password'] == 'abcd':
            print('Pass', data['student'])


app = Flask(__name__)
api = Api(app)

api.add_resource(CheckIn, '/')

