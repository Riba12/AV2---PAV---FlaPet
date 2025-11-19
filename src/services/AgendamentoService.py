from src.repositories.AgendamentoRepository import delete_agendamento, update_agendamento, add_agendamento, get_lista_agendamentos, get_agendamento_by_id

def getAllAgendamentos():
    return get_lista_agendamentos()