import re
from marshmallow import Schema, ValidationError, fields, validates
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs
from sqlalchemy.exc import OperationalError, IntegrityError
from src.services.AnimalService import getAllAnimais, get_animal_by_id, addAnimal, updateAnimal, deleteAnimal

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

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )

class AnimalList(MethodResource, Resource):
    @marshal_with(AnimalResponseSchema(many=True))
    def get(self):
        try:
            animais = getAllAnimais()
            return animais, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AnimalRequestSchema, location=("form"))
    @marshal_with(AnimalResponseSchema)
    def post(self, **kwargs):
        try:
            animal = addAnimal(**kwargs)
            return animal, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

class AnimalItem(MethodResource, Resource):
    @marshal_with(AnimalResponseSchema)
    def get(self, animal_id):
        try:
            animal = get_animal_by_id(animal_id)
            if not animal:
                abort(404, message="Animal not found")
            return animal, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AnimalRequestSchema, location=("form"))
    @marshal_with(AnimalResponseSchema)
    def put(self, animal_id, **kwargs):
        try:
            animal = updateAnimal(id=animal_id, **kwargs)
            return animal, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

    def delete(self, animal_id):
        try:
            animal = deleteAnimal(animal_id)
            if not animal:
                abort(404, message="Animal not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")