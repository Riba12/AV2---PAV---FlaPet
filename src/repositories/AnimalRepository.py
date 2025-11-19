from src.entities.Animal import Animal
from src.entities.Base import db

def get_all_animais() :
    """
    Get all animais stored in the database.

    Returns:
        animais (Animal) -- contains all animais registered.
    """
    #SELECT * FROM ANIMAL
    animais = db.session.query(Animal).all()
    
    return animais

def get_animal_by_id(animal_id: int) -> Animal:
    """
    Get one animal stored in the database.

    Returns:
        animal (Animal) -- find one animal registered.
    """
    # SELECT * FROM ANIMAL WHERE id=animal_id
    animal = db.session.query(Animal).get(animal_id)
    
    return animal

def add_animal(nome: str, especie: str, raca: str, cliente_id: int) -> Animal:
    animal = Animal(nome=nome, especie=especie, raca=raca, cliente_id=cliente_id)
    
    # INSERT INTO ANIMAL values (id, nome, especie, raca, cliente_id)
    db.session.add(animal)

    # Confirma a execução
    db.session.commit()

    return animal

def update_animal(id: int, nome: str, especie: str, raca: str, cliente_id: int) -> Animal:
    """
    Update a Animal in the database.

    Returns:
        animal (Animal) -- updated animal.
    """
    # Verifica se o animal existe
    # SELECT * FROM ANIMAL WHERE id=animal_id
    animal = db.session.query(Animal).get(id)

    if(not animal):
        raise Exception
    
    animal.nome = nome
    animal.especie = especie
    animal.raca = raca
    animal.cliente_id = cliente_id

    db.session.commit()

    return animal

def delete_animal(animal_id) -> Animal:
    """
    Delete one animal stored in the database.

    Returns:
        animal (Animal) -- delete one animal registered.
    """
    animal = db.session.query(Animal).get(animal_id)
    
    if(not animal):
        raise Exception

    # DELETE FROM ANIMAL WHERE id=animal_id
    db.session.delete(animal)

    # Confirma a execução
    db.session.commit()

    return animal