from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.ClienteService import getAllClientes

class ClienteResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    cpf = fields.Str()
    telefone = fields.Str()

class ClienteRequestSchema(Schema):
    nome = fields.Str()
    cpf = fields.Str()
    telefone = fields.Str()

class ClienteList(MethodResource, Resource):
    @marshal_with(ClienteResponseSchema(many=True))
    def get(self):
        try:
            clientes = getAllClientes()
            return clientes, 200
        except OperationalError:
            abort(500, message="Internal Server Error")
