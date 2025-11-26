from src.entities.Agendamento import Agendamento, StatusAgendamento
from src.entities.Base import db
from datetime import datetime
from sqlalchemy import func

def get_lista_agendamentos()-> list:
    """
    Get all agendamentos stored in the database.

    Returns:
        agendamentos (Agendamento) -- contains all agendamentos registered.
    """
    # SELECT * FROM AGENDAMENTO
    # Lista de agendamentos
    agendamentos = db.session.query(Agendamento).all()
    
    return agendamentos

def get_agendamento_by_id(agendamento_id: int)-> Agendamento:
    """
    Get one agendamento stored in the database.

    Returns:
        agendamento (Agendamento) -- find one agendamento registered.
    """
    # SELECT * FROM AGENDAMENTO WHERE id=agendamento_id
    agendamento = db.session.query(Agendamento).get(agendamento_id)
    
    return agendamento

def get_agendamentos_dia_by_animal_id(animal_id: int, data_hora: datetime, ignore_id: int = None) -> list:
    """
    Get all agendamentos for a specific animal for a specific day, ignores cancelado status.

    Returns:
        agendamentos (list) -- list of agendamentos for the given animal for a specific day.
    """
    # SELECT * FROM AGENDAMENTO WHERE animal_id=animal_id AND data_hora=data
    data =data_hora.date()
    agendamentos = db.session.query(Agendamento)\
        .filter(Agendamento.animal_id == animal_id)\
        .filter(func.date(Agendamento.data_hora) == data)\
        .filter(Agendamento.status != StatusAgendamento.CANCELADO)
    if ignore_id:
        agendamentos = agendamentos.filter(Agendamento.id != ignore_id)
    
    return agendamentos.all()

def add_agendamento(data_hora: datetime, animal_id: int, servico_id: int) -> Agendamento:
    """
    Insert a Agendamento in the database.
    Returns:
        agendamento (Agendamento) -- inserted agendamento.
    """

    agendamento = Agendamento(data_hora=data_hora, animal_id=animal_id, servico_id=servico_id)
    
    # INSERT INTO AGENDAMENTO values ( data, animal_id, servico_id)
    db.session.add(agendamento)

    # Confirma a execução
    db.session.commit()

    return agendamento

def update_agendamento(id: int, data_hora: datetime, animal_id: int, servico_id: int) -> Agendamento:
    """
    Update a Agendamento in the database.

    Returns:
        agendamento (Agendamento) -- updated agendamento.
    """
    # Verifica se o agendamento existe
    # SELECT * FROM AGENDAMENTO WHERE id=agendamento_id
    agendamento = db.session.query(Agendamento).get(id)

    if(not agendamento):
        raise Exception
    
    agendamento.data_hora = data_hora
    agendamento.animal_id = animal_id
    agendamento.servico_id = servico_id
    agendamento.status = StatusAgendamento.PENDENTE

    db.session.commit()

    return agendamento

def update_status_agendamento(id: int, status: str) -> Agendamento:
    """
    Update a Agendamento status in the database.

    Returns:
        agendamento (Agendamento) -- updated agendamento.
    """
    # SELECT * FROM AGENDAMENTO WHERE id=agendamento_id
    agendamento = db.session.query(Agendamento).get(id)
    
    agendamento.status = status

    db.session.commit()

    return agendamento