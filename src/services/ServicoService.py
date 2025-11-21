from src.repositories.ServicoRepository import delete_servico, update_servico, add_servico, get_lista_servicos, get_servico_by_id

def getAllServicos():
    return get_lista_servicos()

def getServico(servico_id: int):
    return get_servico_by_id(servico_id)

def addServico(nome: str, descricao: str, valor: float, tempo_minutos: int):
    if valor < 0:
        raise ValueError("Valor do serviço deve ser positivo.")
    if tempo_minutos <= 0:
        raise ValueError("Tempo do serviço deve ser maior que zero.")
    if tempo_minutos > 300:
        raise ValueError("Tempo do serviço deve ser menor que 300 minutos.")
    if nome is None or nome == '':
        raise ValueError("Nome do serviço não pode ser vazio.")
    return add_servico(nome, descricao, valor, tempo_minutos)

def updateServico(id: int, nome: str, descricao: str, valor: float, tempo_minutos: int):
    if valor < 0:
        raise ValueError("Valor do serviço deve ser positivo.")
    if tempo_minutos <= 0:
        raise ValueError("Tempo do serviço deve ser maior que zero.")
    if tempo_minutos > 300:
        raise ValueError("Tempo do serviço deve ser menor que 300 minutos.")
    if nome is None or nome == '':
        raise ValueError("Nome do serviço não pode ser vazio.")
    return update_servico(id=id, nome=nome, descricao=descricao, valor=valor, tempo_minutos=tempo_minutos)

def deleteServico(servico_id: int):
    return delete_servico(servico_id)