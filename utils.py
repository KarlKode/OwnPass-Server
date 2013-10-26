# -*- coding: utf-8 -*-
from flask import request, abort, g, json, Response
from functools import wraps
from hashlib import sha256
from flask.ext.mail import Message
import pygeoip
from twilio.rest import TwilioRestClient
from db import db
from mail import mail

from models import User, Device, Login


def send_device_authentication(device):
    # Send email
    message = Message("OwnPass - New device", recipients=[g.user.email])
    message.html = '''<h1>OwnPass - New device</h1>
<p>A new device with the id %s has tried to log in to your ownpass account.</p>''' % device.code
    print mail.send(message)

    # Send SMS
    account = 'AC70f8a27e5fa47b2e64027c72bf319465'
    token = '5b46fb421f558606e51220d5190e155b'
    client = TwilioRestClient(account, token)

    message = client.messages.create(to=g.user.phone, from_='+18573133734',
                                     body='OwnPass: New device\nID: %s' % device.code)


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
            Device.active, Device.user_id == user.id, Device.device == get_device()).first()
        if not device:
            device = Device(user.id, get_device())
            db.session.add(device)
            db.session.commit()
            send_device_authentication(device)
            return Response(json.dumps({"device": device.device, "id": device.id}), 401)
        # Log ip
        ip = get_ip()
        if not Login.query.filter(Login.user_id == user.id, Login.ip == ip).first():
            login = Login(user.id, ip)
            gi = pygeoip.GeoIP('GeoLiteCity.dat').record_by_addr(ip)
            if gi:
                login.latitude = gi.get('latitude', 0)
                login.longitude = gi.get('longitude', 0)
            db.session.add(login)
            db.session.commit()
        return f(*args, **kwargs)
    return decorated_function


def get_device():
    return sha256(str(request.user_agent)).hexdigest()


def get_ip():
    if request.headers.has_key('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr
