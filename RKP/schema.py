__author__ = 'max'
import hashlib
import os
from app import db


class Member(db.Model):
    __tablename__ = 'messages'
    index = db.Column(db.Integer, primary_key=True)
    rkp = db.Column(db.Integer)
    name = db.Column(db.String(140))
    change = db.Column(db.Integer)
    pos = db.Column(db.Integer)

    def __init__(self, name, rkp):
        self.name = name
        self.rkp = rkp
        self.change = 0
        self.pos = 0


# Create and update all tables and relations - Also commits the all the db stuff!
db.create_all()