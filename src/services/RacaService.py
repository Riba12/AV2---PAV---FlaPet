from src.repositories.RacaRepository import delete_raca, update_raca, add_raca, get_lista_racas, get_raca_by_id
from src.repositories.EspecieRepository import get_especie_by_id

def getAllRacas(especie_id:int=None):
    return get_lista_racas(especie_id)

def getRaca(raca_id: int):
    return get_raca_by_id(raca_id)

def addRaca(nome: str, especie_id: int):

    especie = get_especie_by_id(especie_id)
    if not especie:
        raise ValueError("Especie not found")
    return add_raca(nome, especie_id)

def updateRaca(id: int, nome: str, especie_id: int):
    especie = get_especie_by_id(especie_id)
    if not especie:
        raise ValueError("Especie not found")
    if nome.strip() == "":
        raise ValueError("Nome cannot be empty")
    return update_raca(id=id, nome=nome, especie_id=especie_id)

def deleteRaca(raca_id: int):
    return delete_raca(raca_id)