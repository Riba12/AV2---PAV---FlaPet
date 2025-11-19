from src.entities.Agendamento import Agendamento
from src.entities.Base import db
from datetime import datetime

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

def add_agendamento(data_hora: str, animal_id: int, servico_id: int) -> Agendamento:
    """
    Insert a Agendamento in the database.
    Returns:
        agendamento (Agendamento) -- inserted agendamento.
    """

    data = datetime.fromisoformat(data_hora)
    agendamento = Agendamento(data_hora=data, animal_id=animal_id, servico_id=servico_id)
    
    # INSERT INTO AGENDAMENTO values ( data, animal_id, servico_id)
    db.session.add(agendamento)

    # Confirma a execução
    db.session.commit()

    return agendamento

def update_agendamento(id: int, data_hora: str, animal_id: int, servico_id: int) -> Agendamento:
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
    
    data = datetime.fromisoformat(data_hora)
    agendamento.data_hora = data
    agendamento.animal_id = animal_id
    agendamento.servico_id = servico_id

    db.session.commit()

    return agendamento

def delete_agendamento(agendamento_id: int) -> Agendamento:
    """
    Delete one agendamento stored in the database.

    Returns:
        agendamento (Agendamento) -- deleted agendamento.
    """
    # Verifica se o agendamento existe
    # SELECT * FROM AGENDAMENTO WHERE id=agendamento_id
    agendamento = db.session.query(Agendamento).get(agendamento_id)

    if(not agendamento):
        raise Exception

    # DELETE FROM AGENDAMENTO WHERE id=agendamento_id
    db.session.delete(agendamento)

    # Confirma a execução
    db.session.commit()

    return agendamento 