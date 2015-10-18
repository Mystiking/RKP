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
    members = []
    size = len(temp)
    for m in temp:
        db.session.query(Member).filter(m.index == Member.index).first().pos = size
        size -= 1
    members = db.session.query(Member).order_by(Member.pos).all()
    return render_template('startPage.html', members=members)


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

if __name__ == '__main__':
    app.run(port=1315, debug=True)