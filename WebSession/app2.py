import secrets

from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'It is my secret key'
db = {}


@app.route('/')
def index():
    if 'sid' in session:
        sdata = db.get(session['sid'], {})
    else:
       sdata = {}
    return render_template('index.html', session=sdata)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sid = secrets.token_hex()
        sdata = db.get(sid, {})
        sdata = {'username': request.form['username']}
        db[sid] = sdata
        session['sid'] = sid
        print(session, db, sdata)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'sid' in session:
        db.pop(session['sid'])
        session.pop('sid', None)
    return redirect(url_for('index'))
