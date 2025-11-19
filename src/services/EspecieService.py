from src.repositories.EspecieRepository import delete_especie, update_especie, add_especie, get_lista_especies, get_especie_by_id

def getAllEspecies():
    return get_lista_especies()