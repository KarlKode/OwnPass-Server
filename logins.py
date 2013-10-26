# -*- coding: utf-8 -*-
from flask import g
from flask.ext.restful import Resource, marshal_with
from models import Login
from utils import auth_required


class LoginListResource(Resource):
    @auth_required
    @marshal_with(Login.resource_fields)
    def get(self):
        return g.user.logins.all()
