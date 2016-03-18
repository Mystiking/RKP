from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from schema import *
import datetime, os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'Ultra secret invisible super secret key'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def list_members():
    temp = db.session.query(Member).order_by(Member.rkp).all()
    position = len(temp)
    for m in temp:
        db.session.query(Member).filter(m.index == Member.index).first().pos = position
        position -= 1
    members = db.session.query(Member).order_by(Member.pos).all()
    if 'name' in session:
        return render_template('startPage.html', members=members, unknown=0)
    else:
        return render_template('startPage.html', members=members, unknown=1)

@app.route('/rkp', methods=['GET'])
def follow_the_rules():
    return render_template('rules.html')


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    password = request.form['password']
    if password != 'RKPdealer':
        return redirect('/')
    else:
        members = db.session.query(Member).order_by(Member.name).all()
        return render_template('admin.html', members=members)



@app.route('/login_user', methods=['GET', 'POST'])
def log_in_user():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.name == name).first()
        if user and user.check_pass(password):
            session['name'] = name
            return redirect('/')
    return render_template('login.html',
                           backname='Back to signup',
                           backlink='signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'name' in session:
        del session['name']
    return redirect('/')


@app.route('/go_to', methods=['POST', 'GET'])
def go_to():
    name = request.form['name'].lower()
    pos = int(request.form['position'])
    key = int(request.form['id'])
    print(pos)
    if pos == 1:
        picture = '/static/css/medlemmer/' + name + '/gold_border_' + name + '.png'
    elif pos == 2:
        picture = '/static/css/medlemmer/' + name + '/silver_border_' + name + '.png'
    else:
        picture = '/static/css/medlemmer/' + name + '/' + name + '.png'
    name = name[0].upper() + name[1:]
    messages = db.session.query(Message).filter(Message.key == key).order_by(Message.index).all()
    return render_template('/members/member.html', messages=messages, name=name, picture=picture)



if __name__ == '__main__':
    app.run(port=1315, debug=True)
