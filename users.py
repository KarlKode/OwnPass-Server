# -*- coding: utf-8 -*-
from flask import abort, g
from flask.ext.restful import Resource, reqparse, marshal_with

from db import db
from models import User
from utils import auth_required


user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, location=('json',))
user_parser.add_argument('password', type=str, location=('json',))


class UserListResource(Resource):
    @auth_required
    @marshal_with(User.resource_fields)
    def get(self):
        return User.query.all()

    @marshal_with(User.resource_fields)
    def post(self):
        # Check arguments
        args = user_parser.parse_args()
        if not args['email'] or not args['password']:
            abort(406)
        # Check for duplicate emails
        if User.query.filter(User.email == args['email']).first() is not None:
            abort(409)
        # Add user
        user = User(args['email'], args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class UserResource(Resource):
    @auth_required
    @marshal_with(User.resource_fields)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    @auth_required
    def delete(self, user_id):
        # Users can only delete their own account
        if g.user.id != user_id:
            abort(403)
        # Delete user from the database
        db.session.delete(g.user)
        db.session.commit()
        return '', 204

    @auth_required
    @marshal_with(User.resource_fields)
    def put(self, user_id):
        # Users can only edit their own account
        if g.user.id != user_id:
            abort(403)
        # Check arguments
        args = user_parser.parse_args()
        if not args['email'] or not args['password']:
            abort(406)
        g.user.email = args['email']
        g.user.password = args['password']
        db.session.commit()
        return g.user, 201