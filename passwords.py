# -*- coding: utf-8 -*-
from flask import abort, g
from flask.ext.restful import Resource, reqparse, marshal_with
from db import db
from models import Password
from utils import auth_required


password_parser = reqparse.RequestParser()
password_parser.add_argument('site', type=str, location=('json',))
password_parser.add_argument('username', type=str, location=('json',))
password_parser.add_argument('password', type=str, location=('json',))


class PasswordListResource(Resource):
    @auth_required
    @marshal_with(Password.resource_fields)
    def get(self):
        return g.user.passwords.all()

    @auth_required
    @marshal_with(Password.resource_fields)
    def post(self):
        # Check arguments
        args = password_parser.parse_args()
        if not args['site'] or not args['username'] or not args['password']:
            abort(406)
        # Add password
        password = Password(g.user.id, args['site'], args['username'], args['password'])
        db.session.add(password)
        db.session.commit()
        print password.site
        return password, 201

class PasswordResource(Resource):
    @auth_required
    @marshal_with(Password.resource_fields)
    def get(self, password_id):
        password = Password.get_or_404(password_id)
        if password.user_id != g.user.id:
            abort(404)
        return password

    @auth_required
    def delete(self, password_id):
        # Users can only delete their own passwords
        password = Password.query.get_or_404(password_id)
        if password.user_id != g.user.id:
            abort(404)
        # Delete password from the database
        db.session.delete(password)
        db.session.commit()
        return '', 204

    @auth_required
    @marshal_with(Password.resource_fields)
    def put(self, password_id):
        # Users can only edit their own passwords
        password = Password.query.get_or_404(password_id)
        if password.user_id != g.user.id:
            abort(404)
        # Check arguments
        args = password_parser.parse_args()
        if not args['site'] or not args['username'] or not args['password']:
            abort(406)
        password.site = args['site']
        password.username = args['username']
        password.password = args['password']
        db.session.commit()
        return password, 201
