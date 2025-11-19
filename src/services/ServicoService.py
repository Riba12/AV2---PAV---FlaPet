from src.repositories.ServicoRepository import delete_servico, update_servico, add_servico, get_lista_servicos, get_servico_by_id

def getAllServicos():
    return get_lista_servicos()