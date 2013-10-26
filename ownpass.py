# -*- coding: utf-8 -*-
from flask import Flask, current_app
from flask.ext.restful import Api

from db import db
from devices import DeviceListResource, DeviceResource
from mail import mail
from passwords import PasswordListResource, PasswordResource
from users import UserListResource, UserResource

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
mail.init_app(app)
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'DELETE, GET, HEAD, OPTIONS, POST, PUT')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
    return response

# Debug stuff
@app.route('/install')
def install():
    db.drop_all()
    db.create_all()
    return 'INSTALLED'


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(PasswordListResource, '/passwords')
api.add_resource(PasswordResource, '/passwords/<int:password_id>')
api.add_resource(DeviceListResource, '/devices')
api.add_resource(DeviceResource, '/devices/<int:device_id>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)