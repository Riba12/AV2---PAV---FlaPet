from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from src.repositories import ServicoRepository
from src.repositories import AgendamentoRepository
from src.entities.Agendamento import Agendamento, StatusAgendamento

FUSO_BR = ZoneInfo("America/Sao_Paulo")

def getAllAgendamentos():
    return AgendamentoRepository.get_lista_agendamentos()

def getAgendamentoById(agendamento_id: int):
    return AgendamentoRepository.get_agendamento_by_id(agendamento_id)

def addAgendamento(data_hora: datetime, animal_id: int, servico_id: int):
    try:
        data_hora_inicio = data_hora.replace(tzinfo=FUSO_BR)
    except ValueError:
        raise ValueError("Data em formato inválido. Use o formato ISO 8601: YYYY-MM-DDTHH:MM:SS")
    
    if data_hora_inicio < datetime.now(FUSO_BR):
        raise ValueError("Não é possível agendar um serviço para uma data/hora passada.")
    
    # para saber a duração
    servico = ServicoRepository.get_servico_by_id(servico_id)

    if servico is None:
        raise ValueError("Serviço não encontrado.")
    
    fim = data_hora_inicio + timedelta(minutes=servico.tempo_minutos)

    agendamentos_existentes = AgendamentoRepository.get_agendamentos_dia_by_animal_id(animal_id, data_hora)

    for agendamento in agendamentos_existentes:
        inicio_existente = agendamento.data_hora
        fim_existente = inicio_existente + timedelta(minutes=agendamento.servico.tempo_minutos)

        if (data_hora_inicio < fim_existente) and (fim > inicio_existente):
            raise ValueError("Conflito de agendamento: o animal já possui um agendamento nesse período.")
    return AgendamentoRepository.add_agendamento(data_hora_inicio, animal_id, servico_id)

def updateAgendamento(agendamento_id: int, data_hora: datetime, animal_id: int, servico_id: int):
    try:
        data_hora_inicio = data_hora.replace(tzinfo=FUSO_BR)
    except ValueError:
        raise ValueError("Data em formato inválido. Use o formato ISO 8601: YYYY-MM-DDTHH:MM:SS")
    
    if data_hora_inicio <  datetime.now(FUSO_BR):
        raise ValueError("Não é possível agendar um serviço para uma data/hora passada.")
    
    # para saber a duração
    servico = ServicoRepository.get_servico_by_id(servico_id)

    if servico is None:
        raise ValueError("Serviço não encontrado.")
    
    fim = data_hora_inicio + timedelta(minutes=servico.tempo_minutos)

    agendamentos_existentes = AgendamentoRepository.get_agendamentos_dia_by_animal_id(animal_id, data_hora)

    for agendamento in agendamentos_existentes:

        inicio_existente = agendamento.data_hora.replace(tzinfo=FUSO_BR)
        fim_existente = inicio_existente + timedelta(minutes=agendamento.servico.tempo_minutos)

        if (data_hora_inicio < fim_existente) and (fim > inicio_existente):
            raise ValueError("Conflito de agendamento: o animal já possui um agendamento nesse período.")
    
    return AgendamentoRepository.update_agendamento(agendamento_id, data_hora_inicio, animal_id, servico_id)

def updateStatusAgendamento(agendamento_id: int, status: str):
    try:
        status_enum = StatusAgendamento(status.upper())
    except ValueError:
        raise ValueError("Status inválido para o agendamento.")
    return AgendamentoRepository.update_status_agendamento(agendamento_id, status_enum)