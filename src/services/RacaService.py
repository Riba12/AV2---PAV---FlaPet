from src.repositories.RacaRepository import delete_raca, update_raca, add_raca, get_lista_racas, get_raca_by_id

def getAllRacas():
    return get_lista_racas()
