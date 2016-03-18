from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from schema import *
import datetime, os

@app.route('/load_members', methods=['GET', 'POST'])
def load_m():
    names = db.session.query(Member).order_by(Member.pos).all()
    with open('members.txt') as fp:
        for line in fp:
            flag = 0
            new_member = Member(line, 0)
            for n in names:
                if n.lower() == line.lower():
                    flag = 1
            if flag == 0:
                db.session.add(new_member)
    db.session.commit()
    db.session.flush()
    members = db.session.query(Member).order_by(Member.name).all()
    return render_template('admin.html', members=members)

@app.route('/give_list_rkp', methods=['GET', 'POST'])
def give_list():
    names = (request.form['names'])
    msg = request.form['reason']
    rkp = int(request.form['rkp'])
    members = db.session.query(Member).all()
    names = names.split(", ")
    for n in names:
        db.session.query(Member).filter(Member.name == n).first().rkp += rkp
        db.session.query(Member).filter(Member.name == n).first().latest = msg
        db.session.query(Member).filter(Member.name == n).first().change = rkp
        message = Message(n, msg, db.session.query(Member).filter(Member.name == n).index)
        message.rkp = rkp
        db.session.add(message)
    db.session.commit()
    db.session.flush()
    dir = 'logs'

    if not os.path.exists(dir):
        os.makedirs(dir)

    path = str(datetime.datetime.now())[0:19] + '.txt'
    log = open(os.path.join(dir, path), 'w')
    members = db.session.query(Member).order_by(Member.name).all()
    for m in members:
        log.write(m.name + ' :\n')
        messages = db.session.query(Message).order_by(Message.index).all()
        for msg in messages:
            if msg.key == m.index:
                log.write("Message: " + msg.msg + " RKP : " + str(msg.rkp) + '\n')
    log.close()
    return render_template('admin.html', members=members)



@app.route('/give_rkp', methods=['GET', 'POST'])
def give():
    id = int(request.form['hidden'])
    reason = request.form['reason']
    rkp = int(request.form['amount'])
    members = db.session.query(Member).order_by(Member.name).all()
    db.session.query(Member).filter(Member.index == id).first().rkp += rkp
    db.session.query(Member).filter(Member.index == id).first().latest = reason
    db.session.query(Member).filter(Member.index == id).first().change = rkp
    message = Message(db.session.query(Member).filter(Member.index == id).first().name, reason, id)
    message.rkp = rkp
    db.session.add(message)
    db.session.commit()
    db.session.flush()

    dir = 'logs'

    if not os.path.exists(dir):
        os.makedirs(dir)

    path = str(datetime.datetime.now())[0:19] + '.txt'

    log = open(os.path.join(dir, path), 'w')
    for m in members:
        log.write(m.name + ' :\n')
        messages = db.session.query(Message).order_by(Message.index).all()
        for msg in messages:
            if msg.key == m.index:
                 log.write("Message: " + msg.msg + " RKP : " + str(msg.rkp) + '\n')
    log.close()
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
    with open('members.txt', 'a') as f:
        f.write(name + '\n')
    return render_template('admin.html', members=members)

@app.route('/delete_member', methods=['POST', 'GET'])
def delete_member():
    index = int(request.form['del'])
    db.session.query(Member).filter(Member.index == index).delete()
    db.session.commit()
    members = db.session.query(Member).order_by(Member.pos).all()
    return render_template('admin.html', members=members)



