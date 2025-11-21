from src.repositories.AnimalRepository import delete_animal, update_animal, add_animal, get_all_animais, get_animal_by_id
from src.repositories.EspecieRepository import get_especie_by_id
from src.repositories.RacaRepository import get_raca_by_id
from src.repositories.ClienteRepository import get_cliente_by_id

def getAllAnimais():
    return get_all_animais()

def getAnimal(animal_id: int):
    return get_animal_by_id(animal_id)

def addAnimal(nome: str, especie_id: int, raca_id: int, cliente_id: int):

    if nome is None or nome.strip() == "":
        raise ValueError("Nome cannot be empty")
    if get_especie_by_id(especie_id) is None:
        raise ValueError("Especie does not exist")
    if get_raca_by_id(raca_id) is None:
        raise ValueError("Raca does not exist")
    if get_cliente_by_id(cliente_id) is None:
        raise ValueError("Cliente does not exist")

    return add_animal(nome, especie_id, raca_id, cliente_id)

def updateAnimal(id: int, nome: str, especie_id: int, raca_id: int, cliente_id: int):

    if nome is None or nome.strip() == "":
        raise ValueError("Nome cannot be empty")
    if get_especie_by_id(especie_id) is None:
        raise ValueError("Especie does not exist")
    if get_raca_by_id(raca_id) is None:
        raise ValueError("Raca does not exist")
    if get_cliente_by_id(cliente_id) is None:
        raise ValueError("Cliente does not exist")

    return update_animal(id, nome, especie_id, raca_id, cliente_id)

def deleteAnimal(animal_id: int):
    return delete_animal(animal_id)