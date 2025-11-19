from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.EspecieService import getAllEspecies

class EspecieResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()

class EspecieRequestSchema(Schema):
    nome = fields.Str()

class EspecieList(MethodResource, Resource):
    @marshal_with(EspecieResponseSchema(many=True))
    def get(self):
        try:
            especies = getAllEspecies()
            return especies, 200
        except OperationalError:
            abort(500, message="Internal Server Error")