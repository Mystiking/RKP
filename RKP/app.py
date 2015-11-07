from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from schema import *
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'Ultra secret invisible super secret key'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def list_members():
    temp = db.session.query(Member).order_by(Member.rkp).all()
    size = len(temp)
    for m in temp:
        db.session.query(Member).filter(m.index == Member.index).first().pos = size
        size -= 1
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
        members = db.session.query(Member).order_by(Member.pos).all()
        return render_template('admin.html', members=members)


@app.route('/give_rkp', methods=['GET', 'POST'])
def give():
    id = int(request.form['hidden'])
    reason = request.form['reason']
    rkp = int(request.form['amount'])
    members = db.session.query(Member).order_by(Member.pos).all()
    db.session.query(Member).filter(Member.index == id).first().rkp += rkp
    db.session.query(Member).filter(Member.index == id).first().latest = reason
    db.session.query(Member).filter(Member.index == id).first().change = rkp
    message = Message(db.session.query(Member).filter(Member.index == id).first().name, reason, id)
    message.rkp = rkp
    db.session.add(message)
    db.session.commit()
    db.session.flush()
    return render_template('admin.html', members=members)


@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['member']
    rkp = int(request.form['rkp'])
    new_member = Member(name, rkp)
    members = db.session.query(Member).order_by(Member.pos).all()
    for m in members:
        if m.name == name:
            return render_template('admin.html', members=members)
    db.session.add(new_member)
    db.session.flush()
    db.session.commit()
    members = db.session.query(Member).order_by(Member.pos).all()
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


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if not db.session.query(User).filter(User.name == name).first():
            db.session.add(User(name, password))
            db.session.commit()
            return redirect('/login_user')
    return render_template('signup.html')


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
    html = '/members/' + name + '.html'
    print(pos)
    if pos == 1:
        picture = '/static/css/medlemmer/' + name + '/gold_border_' + name + '.png'
    elif pos == 2:
        picture = '/static/css/medlemmer/' + name + '/silver_border_' + name + '.png'
    else:
        picture = '/static/css/medlemmer/' + name + '/' + name + '.png'
    name = name[0].upper() + name[1:]
    messages = db.session.query(Message).filter(Message.key == key).order_by(Message.index).all()
    return render_template(html, messages=messages, name=name, picture=picture)



@app.route('/delete_member', methods=['POST', 'GET'])
def delete_member():
    index = int(request.form['del'])
    db.session.query(Member).filter(Member.index == index).delete()
    db.session.commit()
    members = db.session.query(Member).order_by(Member.pos).all()
    return render_template('admin.html', members=members)


if __name__ == '__main__':
    app.run(port=1315, debug=True)