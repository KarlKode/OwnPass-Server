# -*- coding: utf-8 -*-
import datetime
import random
from flask.ext.restful import fields
from db import db


class User(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'email': fields.String,
        'phone': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


class Password(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'site': fields.String,
        'username': fields.String,
        'password': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('passwords', lazy='dynamic'))
    site = db.Column(db.String(200))
    username = db.Column(db.LargeBinary())
    password = db.Column(db.LargeBinary())

    def __init__(self, user_id, site, username, password):
        self.user_id = user_id
        self.site = site
        self.username = username
        self.password = password


class Device(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'device': fields.String,
        'active': fields.Boolean
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('devices', lazy='dynamic'))
    device = db.Column(db.String(64))
    active = db.Column(db.Boolean)
    code = db.Column(db.Integer)

    def __init__(self, user_id, device):
        self.user_id = user_id
        self.device = device
        self.active = False
        self.code = random.randint(0, 1000000)


class Login(db.Model):
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'ip': fields.String,
        'time': fields.DateTime,
        'latitude': fields.String,
        'longitude': fields.String
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('logins', lazy='dynamic'))
    ip = db.Column(db.String(15))
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, user_id, ip):
        self.user_id = user_id
        self.ip = ip
