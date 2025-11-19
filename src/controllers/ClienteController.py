import re
from marshmallow import Schema, ValidationError, fields, validates
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.ClienteService import getAllClientes, get_cliente_by_id

class ClienteResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    cpf = fields.Str()
    telefone = fields.Str()

class ClienteRequestSchema(Schema):
    nome = fields.Str()
    cpf = fields.Str()
    telefone = fields.Str()

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )

class ClienteList(MethodResource, Resource):
    @marshal_with(ClienteResponseSchema(many=True))
    def get(self):
        try:
            clientes = getAllClientes()
            return clientes, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

class ClienteItem(MethodResource, Resource):
    @marshal_with(ClienteResponseSchema)
    def get(self, cliente_id):
        try:
            cliente = get_cliente_by_id(cliente_id)
            if not cliente:
                abort(404, message="Cliente not found")
            return cliente, 200
        except OperationalError:
            abort(500, message="Internal Server Error")
