from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'It is my secret key'

@app.route('/')
def index():
    print(session)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        print(session)
        return redirect(url_for('index'))
    print(session)
    return render_template('login.html')
