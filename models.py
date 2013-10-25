# -*- coding: utf-8 -*-
from db import db


class User(db.Model):
    _to_serialize = ('id', 'email')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


class Password(db.Model):
    _to_serialize = ('id', 'user_id', 'url', 'username', 'password')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('passwords', lazy='dynamic'))
    url = db.Column(db.String(200))
    username = db.Column(db.LargeBinary())
    password = db.Column(db.LargeBinary())

    def __init__(self, user_id, url, username, password):
        self.user_id = user_id
        self.url = url
        self.username = username
        self.password = password
