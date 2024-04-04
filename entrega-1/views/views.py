from models.models import *
from datetime import datetime
from flask import request
from flask_restful import Resource


blackList_schema = BlacklistSchema()
blackLists_schema = BlacklistSchema(many=True)


def check_required_fields(required_fields):
    error = False
    fields_missing = []
    for field in required_fields:
        if field not in request.json:
            error = True
            fields_missing.append(field)

    return error, f"los campos {', '.join(fields_missing)} son obligatorios"


class ViewHealthCheck(Resource):
    def get(self):
        return 'pong', 200


class ViewGetBlacklist(Resource):
    def get(self, email):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400

        email = Blacklist.query.filter_by(email=email).first()
        if email:
            return {
                'is_blacklisted': True,
                'reason': email.blocked_reason,
            }, 200
        else:
            return {
                'is_blacklisted': False,
                'reason': None,
            }, 404


class ViewCreateBlacklist(Resource):
    def post(self):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400

        required_fields = ['email', 'app_uuid', 'blocked_reason']
        error, message = check_required_fields(required_fields)
        if error:
            return {'error': message}, 400

        user_ip = request.remote_addr
        if not user_ip:
            return {'error': 'No se puede obtener la IP de la solicitud.'}, 400

        email = request.json.get('email')
        if Blacklist.query.filter_by(email=email).first():
            return {'error': 'El email ya se encuentra en la lista'}, 412

        now = datetime.now()
        new_blacklist_email = Blacklist(
            email=email,
            app_uuid=request.json.get('app_uuid'),
            blocked_reason=request.json.get('blocked_reason'),
            created_at=now,
            user_ip=user_ip
        )
        db.session.add(new_blacklist_email)
        db.session.commit()
        return {'msg': 'el email fue agregado correctamente'}, 201


class ResetDatabase(Resource):
    def post(self):
        db.session.query(Blacklist).delete()
        db.session.commit()
        return {'msg': 'All data has been deleted'}, 200