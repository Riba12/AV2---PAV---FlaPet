from marshmallow import Schema, fields
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs
from sqlalchemy.exc import OperationalError, IntegrityError
from src.services.AgendamentoService import getAllAgendamentos, getAgendamentoById, addAgendamento, updateAgendamento, updateStatusAgendamento

class AgendamentoResponseSchema(Schema):
    id = fields.Int()
    data_hora = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    animal_nome = fields.Str(attribute="animal.nome")
    animal_id = fields.Int(attribute="animal.id")
    servico_nome = fields.Str(attribute="servico.nome")
    servico_id = fields.Int(attribute="servico.id")
    status = fields.Method("get_status")

    def get_status(self, obj):
        return obj.status.name

class AgendamentoRequestSchema(Schema):
    data_hora = fields.DateTime()
    animal_id = fields.Int()
    servico_id = fields.Int()

class AgendamentoList(MethodResource, Resource):
    @marshal_with(AgendamentoResponseSchema(many=True))
    def get(self):
        try:
            agendamentos = getAllAgendamentos()
            return agendamentos, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AgendamentoRequestSchema, location=("form"))
    @marshal_with(AgendamentoResponseSchema)
    def post(self, **kwargs):
        try:
            agendamento = addAgendamento(**kwargs)
            return agendamento, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

class AgendamentoItem(MethodResource, Resource):
    @marshal_with(AgendamentoResponseSchema)
    def get(self, agendamento_id):
        try:
            agendamento = getAgendamentoById(agendamento_id)
            if not agendamento:
                abort(404, message="Agendamento not found")
            return agendamento, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AgendamentoRequestSchema, location=("form"))
    @marshal_with(AgendamentoResponseSchema)
    def put(self, agendamento_id, **kwargs):
        try:
            agendamento = updateAgendamento(agendamento_id, **kwargs)
            return agendamento, 200
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        except ValueError as err:
            abort(400, message=str(err))
    
    @use_kwargs({'status': fields.Str(required=True)}, location=("form"))
    @marshal_with(AgendamentoResponseSchema)
    def patch(self, agendamento_id, **kwargs):
        try:
            agendamento = updateStatusAgendamento(agendamento_id, kwargs['status'])
            return agendamento, 200
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        except ValueError as err:
            abort(400, message=str(err))