from src.entities.Especie import Especie
from src.entities.Base import db

def get_lista_especies()-> list:
    """
    Get all especies stored in the database.

    Returns:
        especies (Especie) -- contains all especies registered.
    """
    # SELECT * FROM ESPECIE
    # Lista de especies
    especies = db.session.query(Especie).all()
    
    return especies

def get_especie_by_id(especie_id:str)-> Especie:
    """
    Get one especie stored in the database.

    Returns:
        especie (Especie) -- find one especie registered.
    """
    # SELECT * FROM ESPECIE WHERE id=especie_id
    especie = db.session.query(Especie).get(especie_id)
    
    return especie

def add_especie(nome: str) -> Especie:
    """
    Insert a Especie in the database.
    Returns:
        especie (Especie) -- inserted especie.
    """
    especie = Especie(nome=nome)
    
    # INSERT INTO ESPECIE values (id, nome)
    db.session.add(especie)

    # Confirma a execução
    db.session.commit()

    return especie

def update_especie(id: int, nome: str) -> Especie:
    """
    Update a Especie in the database.

    Returns:
        especie (Especie) -- updated especie.
    """
    # Verifica se a especie existe
    # SELECT * FROM ESPECIE WHERE id=especie_id
    especie = db.session.query(Especie).get(id)

    if(not especie):
        raise Exception
    
    especie.nome = nome

    db.session.commit()

    return especie

def delete_especie(especie_id) -> Especie:
    """
    Delete one especie stored in the database.

    Returns:
        especie (Especie) -- deleted especie.
    """
    # Verifica se a especie existe
    # SELECT * FROM ESPECIE WHERE id=especie_id
    especie = db.session.query(Especie).get(especie_id)
    db.session.delete(especie)
    db.session.commit()
    return especie