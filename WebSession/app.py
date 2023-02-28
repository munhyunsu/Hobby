from flask import Flask

app = Flask(__name__)
app.secret_key = 'It is my secret key'
