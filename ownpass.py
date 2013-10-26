# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Api

from db import db
from passwords import PasswordListResource, PasswordResource
from users import UserListResource, UserResource

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
api = Api(app)

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


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(PasswordListResource, '/passwords')
api.add_resource(PasswordResource, '/passwords/<int:password_id>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)