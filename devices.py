# -*- coding: utf-8 -*-
from flask import g
from flask.ext.restful import Resource, marshal_with, abort, reqparse
from db import db
from models import Device
from utils import auth_required


device_parser = reqparse.RequestParser()
device_parser.add_argument('device', type=str, location=('json',))
device_parser.add_argument('active', type=bool, location=('json',))
device_parser.add_argument('code', type=str, location=('json',))


class DeviceListResource(Resource):
    @auth_required
    @marshal_with(Device.resource_fields)
    def get(self):
        return g.user.devices.all()

class DeviceResource(Resource):
    @auth_required
    @marshal_with(Device.resource_fields)
    def get(self, device_id):
        device = Device.query.get_or_404(device_id)
        if device.user_id != g.user.id:
            abort(404)
        return device

    @auth_required
    def delete(self, device_id):
        # Users can only delete their own devices
        device_id = Device.query.get_or_404(device_id)
        if device_id.user_id != g.user.id:
            abort(404)
        # Delete device from the database
        db.session.delete(device_id)
        db.session.commit()
        return '', 204

    @auth_required
    @marshal_with(Device.resource_fields)
    def put(self, device_id):
        # Users can only edit their own devices
        device = Device.query.get_or_404(device_id)
        if device.user_id != g.user.id:
            abort(404)
        args = device_parser.parse_args()
        # Check device code
        if device.code != args['code']:
            abort(404)
        # Check arguments
        if not args['device'] or not args['active']:
            abort(406)
        device.device = args['device']
        device.active = args['active']
        db.session.commit()
        return device, 201
