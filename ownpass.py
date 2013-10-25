# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.rest import RESTResource

from db import db
from passwords import PasswordHandler
from users import UserHandler

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)

# Debug stuff
@app.route('/install')
def install():
    db.drop_all()
    db.create_all()

    from models import User, Password
    from pbkdf2 import crypt
    u1 = User('marc@marcg.ch', crypt('cat_and_mouse'))
    db.session.add(u1)
    db.session.commit()

    p1 = Password(u1.id, 'http://www.google.com/', 'test-user', 'test-password')
    db.session.add(p1)
    db.session.commit()

    return 'INSTALLED'


user_resource = RESTResource(
    name='user',
    route='/users',
    app=app,
    actions=['add', 'update', 'delete', 'list'],
    handler=UserHandler()
)

password_resource = RESTResource(
    name='password',
    route='/passwords',
    app=app,
    actions=['add', 'update', 'delete', 'list'],
    handler=PasswordHandler()
)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)