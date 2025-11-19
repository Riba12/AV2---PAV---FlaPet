from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.AnimalService import getAllAnimais

class AnimalResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    idade = fields.Int()
    cliente_id = fields.Int()
    especie_id = fields.Int()
    raca_id = fields.Int()

class AnimalRequestSchema(Schema):
    nome = fields.Str()
    idade = fields.Int()
    cliente_id = fields.Int()
    especie_id = fields.Int()
    raca_id = fields.Int()

class AnimalList(MethodResource, Resource):
    @marshal_with(AnimalResponseSchema(many=True))
    def get(self):
        try:
            animais = getAllAnimais()
            return animais, 200
        except OperationalError:
            abort(500, message="Internal Server Error")