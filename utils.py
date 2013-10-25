# -*- coding: utf-8 -*-
from flask import request

from models import User


def check_auth(*args, **kwargs):
    auth = request.authorization
    user = User.query.filter(User.email == auth.username, User.password == auth.password).first()
    if not user:
        return False
    return user
