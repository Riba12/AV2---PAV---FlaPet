from src.entities.Raca import Raca
from src.entities.Base import db

def get_lista_racas() -> list:
    """
    Get all racas stored in the database.

    Returns:
        racas (Raca) -- contains all racas registered.
    """
    # SELECT * FROM RACA
    # Lista de racas
    racas = db.session.query(Raca).all()
    
    return racas

def get_raca(raca_id: int) -> Raca:
    """
    Get one raca stored in the database.

    Returns:
        raca (Raca) -- find one raca registered.
    """
    # SELECT * FROM RACA WHERE id=raca_id
    raca = db.session.query(Raca).get(raca_id)
    
    return raca

def add_raca(nome: str, especie_id: int) -> Raca:
    """
    Insert a Raca in the database.
    Returns:
        raca (Raca) -- inserted raca.
    """
    raca = Raca(nome=nome, especie_id=especie_id)
    
    # INSERT INTO RACA values (id, nome)
    db.session.add(raca)

    # Confirma a execução
    db.session.commit()

    return raca

def update_raca(id: int, nome: str, especie_id: int) -> Raca:
    """
    Update a Raca in the database.

    Returns:
        raca (Raca) -- updated raca.
    """
    # Verifica se a raca existe
    # SELECT * FROM RACA WHERE id=raca_id
    raca = db.session.query(Raca).get(id)

    if(not raca):
        raise Exception
    
    raca.nome = nome
    raca.especie_id = especie_id

    db.session.commit()

    return raca

def delete_raca(raca_id: int) -> Raca:
    """
    Delete one raca stored in the database.

    Returns:
        raca (Raca) -- deleted raca.
    """
    # Verifica se a raca existe
    # SELECT * FROM RACA WHERE id=raca_id
    raca = db.session.query(Raca).get(raca_id)

    if(not raca):
        raise Exception

    # DELETE FROM RACA WHERE id=raca_id
    db.session.delete(raca)

    db.session.commit()

    return raca