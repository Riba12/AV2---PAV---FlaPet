import re
from marshmallow import Schema, ValidationError, fields, validates
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.RacaService import getAllRacas, get_raca_by_id

class RacaResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    especie_id = fields.Int()

class RacaRequestSchema(Schema):
    nome = fields.Str()
    especie_id = fields.Int() 

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )  

class RacaList(MethodResource, Resource):
    @marshal_with(RacaResponseSchema(many=True))
    def get(self):
        try:
            racas = getAllRacas()
            return racas, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

class RacaItem(MethodResource, Resource):
    @marshal_with(RacaResponseSchema)
    def get(self, raca_id):
        try:
            raca = get_raca_by_id(raca_id)
            if not raca:
                abort(404, message="Raca not found")
            return raca, 200
        except OperationalError:
            abort(500, message="Internal Server Error")