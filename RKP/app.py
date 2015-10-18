from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from schema import *
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'Ultra secret invisible super secret key'
db = SQLAlchemy(app)


@app.route('/', methods=['POST'])
def new_msg():
    if 'name' not in session:
        return redirect('/login_user')
    msg = request.form['message']
    db.session.add(Message(session['name'], msg))
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['GET'])
def list_members():
    posts = db.session.query(Message).order_by(Message.index).all()
    while len(posts) > 10:
        db.session.delete(posts[0])
        posts = posts[1:]
        db.session.commit()
    temp = db.session.query(Member).order_by(Member.rkp).all()
    size = len(temp)
    for m in temp:
        db.session.query(Member).filter(m.index == Member.index).first().pos = size
        size -= 1
    members = db.session.query(Member).order_by(Member.pos).all()
    if 'name' in session:
        return render_template('startPage.html', members=members, posts=posts, name=session['name'], unknown=0)
    else:
        return render_template('startPage.html', members=members, posts=posts, name='no name', unknown=1)


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
    rkp = int(request.form['amount'])
    members = db.session.query(Member).order_by(Member.pos).all()
    db.session.query(Member).filter(Member.index == id).first().rkp += rkp
    db.session.commit()
    print(id, rkp)
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

if __name__ == '__main__':
    app.run(port=1315, debug=True)