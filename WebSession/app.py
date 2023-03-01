from flask import Flask, session, render_template

app = Flask(__name__)
app.secret_key = 'It is my secret key'

@app.route('/')
def index():
    return render_template('index.html')
