from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from schema import *
import datetime, os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SERVER_NAME'] = 'guldda.me'
app.config['DEBGUG'] = False
app.secret_key = 'Ultra secret invisible super secret key'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def list_members():
    temp = db.session.query(Member).order_by(Member.rkp).all()
    position = 1
    for m in temp:
        db.session.query(Member).filter(m.index == Member.index).first().pos = position
        position += 1
    members = db.session.query(Member).order_by(Member.pos).all()
    if 'name' in session:
        return render_template('startPage.html', members=members, unknown=0)
    else:
        return render_template('startPage.html', members=members, unknown=1)

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


@app.route('/give_list_rkp', methods=['GET', 'POST'])
def give_list():
    print("Anything?")
    names = (request.form['names'])
    print("Names: " + names)
    msg = request.form['reason']
    print(msg)
    rkp = int(request.form['rkp'])
    print(rkp)
    members = db.session.query(Member).all()
    print(names)
    names = names.split(", ")
    for n in names:
        print("Entered for loop...")
        db.session.query(Member).filter(Member.name == n).first().rkp += rkp
        print("rkp sat")
        db.session.query(Member).filter(Member.name == n).first().latest = msg
        print("msg sat")
        db.session.query(Member).filter(Member.name == n).first().change = rkp
        print("change sat")
        message = Message(n, msg, db.session.query(Member).filter(Member.name == n).index)
        print("created message")
        message.rkp = rkp
        print("added rkp to message")
        db.session.add(message)
        print("added message to db")
    db.session.commit()
    db.session.flush()
    print("Starting logging...")
    dir = 'logs'

    if not os.path.exists(dir):
        os.makedirs(dir)

    path = str(datetime.datetime.now())[0:19] + '.txt'
    log = open(os.path.join(dir, path), 'w')
    members = db.session.query(Members).order_by(Member.name).all()
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



@app.route('/delete_member', methods=['POST', 'GET'])
def delete_member():
    index = int(request.form['del'])
    db.session.query(Member).filter(Member.index == index).delete()
    db.session.commit()
    members = db.session.query(Member).order_by(Member.pos).all()
    return render_template('admin.html', members=members)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
