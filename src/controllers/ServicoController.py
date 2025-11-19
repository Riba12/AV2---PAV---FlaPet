import re
from marshmallow import Schema, ValidationError, fields, validates
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.ServicoService import getAllServicos, get_servico_by_id

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

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )

class ServicoList(MethodResource, Resource):
    @marshal_with(ServicoResponseSchema(many=True))
    def get(self):
        try:
            servicos = getAllServicos()
            return servicos, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

class ServicoItem(MethodResource, Resource):
    @marshal_with(ServicoResponseSchema)
    def get(self, servico_id):
        try:
            servico = get_servico_by_id(servico_id)
            if not servico:
                abort(404, message="Servico not found")
            return servico, 200
        except OperationalError:
            abort(500, message="Internal Server Error")