from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.RacaService import getAllRacas

class RacaResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    especie_id = fields.Int()

class RacaRequestSchema(Schema):
    nome = fields.Str()
    especie_id = fields.Int()   

class RacaList(MethodResource, Resource):
    @marshal_with(RacaResponseSchema(many=True))
    def get(self):
        try:
            racas = getAllRacas()
            return racas, 200
        except OperationalError:
            abort(500, message="Internal Server Error")