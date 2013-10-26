# -*- coding: utf-8 -*-
from flask import request
from flask.ext.rest import need_auth

from db import db
from models import User
from utils import check_auth


class UserHandler(object):
    def check_user_json(self):
        if not request.json or not request.json.has_key('email') or not request.json.has_key('password'):
            return False
        return True

    def add(self):
        # Validate request
        if not self.check_user_json():
            return 400, 'Invalid request'
        # Get JSON request data
        email = request.json.get('email')
        password = request.json.get('password')
        # Check for duplicate emails
        if User.query.filter(User.email == email).first() is not None:
            return 400, 'Invalid request'
        # Add user
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        return 200, user

    @need_auth(check_auth, 'user')
    def update(self, user):
        if not self.check_user_json():
            return 400, 'Invalid request'
        user.email = request.json['email']
        user.password = request.json['password']
        db.session.commit()
        return 200, user

    @need_auth(check_auth, 'user')
    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
        return 200, 'OK'

    @need_auth(check_auth, remove_attr=False)
    def list(self):
        users = User.query.all()
        return 200, users
