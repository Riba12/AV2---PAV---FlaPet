from src.repositories.EspecieRepository import delete_especie, update_especie, add_especie, get_lista_especies, get_especie_by_id

def getAllEspecies():
    return get_lista_especies()

def getEspecie(especie_id: int):
    return get_especie_by_id(especie_id)

def addEspecie(nome: str):
    if nome is None or nome == '':
        raise ValueError("Nome da espécie não pode ser vazio.")
    return add_especie(nome)

def updateEspecie(id: int, nome: str):
    if nome is None or nome == '':
        raise ValueError("Nome da espécie não pode ser vazio.")
    return update_especie(id=id, nome=nome)

def deleteEspecie(especie_id: int):
    return delete_especie(especie_id)