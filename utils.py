# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import request, abort, g, current_app, make_response
from functools import wraps, update_wrapper

from models import User


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.authorization:
            return abort(401)
        auth = request.authorization
        user = User.query.filter(User.email == auth.username, User.password == auth.password).first()
        if not user:
            return abort(401)
        g.user = user
        return f(*args, **kwargs)
    return decorated_function
