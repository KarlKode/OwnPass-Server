# -*- coding: utf-8 -*-
from flask import request
from flask.ext.rest import need_auth
from db import db
from models import Password
from utils import check_auth


class PasswordHandler(object):
    @need_auth(check_auth, 'user', remove_attr=False)
    def add(self, user):
        # Validate request
        if not (request.json and request.json.has_key('url') and request.json.has_key('username') and request.json.has_key('password')):
            return 400, 'Invalid request'
        # Get JSON request data
        url = request.json.get('url')
        username = request.json.get('username')
        password_string = request.json.get('password')
        # Add password
        password = Password(user.id, url, username, password_string)
        db.session.add(password)
        db.session.commit()
        return 200, password

    def update(self):
        pass

    def delete(self):
        pass

    @need_auth(check_auth, 'user', remove_attr=False)
    def list(self, user):
        passwords = user.passwords.all()
        return 200, passwords
