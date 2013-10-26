# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import request, abort, g
from functools import wraps
from hashlib import sha256
from flask.ext.mail import Message
from db import db
from mail import mail

from models import User, Device


def send_device_authentication(device):
    message = Message("OwnPass - New device", recipients=[g.user.email])
    message.html = '''<h1>OwnPass - New device</h1>
<p>A new device with the id %d has tried to log in to your ownpass account.</p>''' % device.id
    print mail.send(message)


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.authorization:
            return abort(401)
        auth = request.authorization
        # Check user
        user = User.query.filter(User.email == auth.username, User.password == auth.password).first()
        if not user:
            return abort(401)
        g.user = user
        # Device allowed?
        device = Device.query.filter(
            Device.active == True, Device.user_id == user.id, Device.device == get_device()).first()
        if not device:
            device = Device(user.id, get_device())
            db.session.add(device)
            db.session.commit()
            send_device_authentication(device)
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


def get_device():
    return sha256(str(request.user_agent)).hexdigest()