from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.ServicoService import getAllServicos

class ServicoResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    descricao = fields.Str()
    preco = fields.Float()
    tempo_minutos = fields.Int()

class ServicoRequestSchema(Schema):
    nome = fields.Str()
    descricao = fields.Str()
    preco = fields.Float()
    tempo_minutos = fields.Int()

class ServicoList(MethodResource, Resource):
    @marshal_with(ServicoResponseSchema(many=True))
    def get(self):
        try:
            servicos = getAllServicos()
            return servicos, 200
        except OperationalError:
            abort(500, message="Internal Server Error")