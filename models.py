# -*- coding: utf-8 -*-
from flask.ext.restful import fields
from db import db


class User(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'email': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


class Password(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'site:': fields.String,
        'email': fields.String,
        'password': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('passwords', lazy='dynamic'))
    site = db.Column(db.String(200))
    username = db.Column(db.LargeBinary())
    password = db.Column(db.LargeBinary())

    def __init__(self, user_id, url, username, password):
        self.user_id = user_id
        self.site = url
        self.username = username
        self.password = password
