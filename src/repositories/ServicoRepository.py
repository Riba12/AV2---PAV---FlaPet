from src.entities.Servico import Servico
from src.entities.Base import db

def get_lista_servicos()-> list:
    """
    Get all servicos stored in the database.

    Returns:
        servicos (Servico) -- contains all servicos registered.
    """
    # SELECT * FROM SERVICO
    # Lista de servicos
    servicos = db.session.query(Servico).all()
    
    return servicos

def get_servico_by_id(servico_id:str)-> Servico:
    """
    Get one servico stored in the database.

    Returns:
        servico (Servico) -- find one servico registered.
    """
    # SELECT * FROM SERVICO WHERE id=servico_id
    servico = db.session.query(Servico).get(servico_id)
    
    return servico  

def add_servico(nome: str,descricao: str, valor: float, tempo_minutos: int) -> Servico:
    """
    Insert a Servico in the database.
    Returns:
        servico (Servico) -- inserted servico.
    """
    servico = Servico(nome=nome, descricao=descricao, valor=valor, tempo_minutos=tempo_minutos)
    
    # INSERT INTO SERVICO values (id, nome, descricao, valor, tempo_minutos)
    db.session.add(servico)

    # Confirma a execução
    db.session.commit()

    return servico

def update_servico(id: int, nome: str, descricao: str, valor: float, tempo_minutos: int) -> Servico:
    """
    Update a Servico in the database.

    Returns:
        servico (Servico) -- updated servico.
    """
    # Verifica se o servico existe
    # SELECT * FROM SERVICO WHERE id=servico_id
    servico = db.session.query(Servico).get(id)

    if(not servico):
        raise Exception
    
    servico.nome = nome
    servico.descricao = descricao
    servico.valor = valor
    servico.tempo_minutos = tempo_minutos

    db.session.commit()

    return servico

def delete_servico(servico_id: int)-> Servico:
    """
    Delete one servico stored in the database.

    Returns:
        servico (Servico) -- deleted servico.
    """
    # Verifica se o servico existe
    # SELECT * FROM SERVICO WHERE id=servico_id
    servico = db.session.query(Servico).get(servico_id)

    if(not servico):
        raise Exception

    # DELETE FROM SERVICO WHERE id=servico_id
    db.session.delete(servico)

    db.session.commit()

    return servico