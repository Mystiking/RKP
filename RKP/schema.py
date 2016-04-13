__author__ = 'max'
import hashlib
import os
from app import db


class Member(db.Model):
    '''
    An object to store data about RKG-members
    '''
    __tablename__ = 'members'
    index = db.Column(db.Integer, primary_key=True)

    # RKP points
    rkp = db.Column(db.Integer)

    # Member name
    name = db.Column(db.String(140))

    # Lastest change message and rkp
    latest = db.Column(db.String(140))
    change = db.Column(db.Integer)

    # ?
    pos = db.Column(db.Integer)

    # Balance in rkgnskab
    balance = db.Column(db.Integer)

    def __init__(self, name, rkp):
        self.name = name
        self.rkp = rkp
        self.change = 0
        self.pos = 0
        self.balance = 0
        self.latest = 'Ingen begrundelse'


class Balance_action(db.Model):
    '''
    Used to change the balance of memebers
    '''
    __tablename__ = 'balance_actions'
    index = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(140))
    name = db.Column(db.String(140))
    member_id = db.Column(db.Integer)
    balance_change = db.Column(db.Integer)

    def __init__(self, name, reason, member_id, balance_change):
        self.name = name
        self.reason = reason
        self.member_id = member_id
        self.balance_change = balance_change

class Message(db.Model):
    '''
    Used for communication on the site
    '''
    __tablename__ = 'messages'
    index = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(140))
    name = db.Column(db.String(140))
    key = db.Column(db.Integer)
    rkp = db.Column(db.Integer)

    def __init__(self, name, msg, key):
        self.name = name
        self.msg = msg
        self.key = key


class User(db.Model):
    '''
    I have no idea what this is used for
    '''
    __tablename__ = 'users'
    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.Binary(32))
    salt = db.Column(db.Binary(32))

    def __init__(self, name, password):
        self.name = name
        self.salt = os.urandom(32)
        self.password = hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000)

    def check_pass(self, password):
        return self.password == hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000)


# Create and update all tables and relations - Also commits the all the db stuff!
db.create_all()
