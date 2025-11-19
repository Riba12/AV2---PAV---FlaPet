import re
from marshmallow import Schema, ValidationError, fields, validates
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with
from sqlalchemy.exc import OperationalError
from src.services.EspecieService import getAllEspecies, get_especie_by_id

class EspecieResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()

class EspecieRequestSchema(Schema):
    nome = fields.Str()

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )

class EspecieList(MethodResource, Resource):
    @marshal_with(EspecieResponseSchema(many=True))
    def get(self):
        try:
            especies = getAllEspecies()
            return especies, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

class EspecieItem(MethodResource, Resource):
    @marshal_with(EspecieResponseSchema)
    def get(self, especie_id):
        try:
            especie = get_especie_by_id(especie_id)
            if not especie:
                abort(404, message="Especie not found")
            return especie, 200
        except OperationalError:
            abort(500, message="Internal Server Error")