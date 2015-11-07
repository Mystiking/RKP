__author__ = 'max'
import hashlib
import os
from app import db


class Member(db.Model):
    __tablename__ = 'members'
    index = db.Column(db.Integer, primary_key=True)
    rkp = db.Column(db.Integer)
    name = db.Column(db.String(140))
    latest = db.Column(db.String(140))
    change = db.Column(db.Integer)
    pos = db.Column(db.Integer)

    def __init__(self, name, rkp):
        self.name = name
        self.rkp = rkp
        self.change = 0
        self.pos = 0
        self.latest = 'None given'


class Message(db.Model):
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