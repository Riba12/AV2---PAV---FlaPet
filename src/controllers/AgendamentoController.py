from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.AgendamentoService import getAllAgendamentos

class AgendamentoResponseSchema(Schema):
    id = fields.Int()
    data_hora = fields.DateTime()
    animal_id = fields.Int()
    servico_id = fields.Int()
    status = fields.Str()

class AgendamentoRequestSchema(Schema):
    data_hora = fields.DateTime()
    animal_id = fields.Int()
    servico_id = fields.Int()

class AgendamentoList(MethodResource, Resource):
    @marshal_with(AgendamentoResponseSchema(many=True))
    def get(self):
        try:
            agendamentos = getAllAgendamentos()
            return agendamentos, 200
        except OperationalError:
            abort(500, message="Internal Server Error")