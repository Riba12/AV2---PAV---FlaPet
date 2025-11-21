from src.repositories.ClienteRepository import delete_cliente, update_cliente, add_cliente, get_all_clientes, get_cliente_by_id, get_cliente_by_cpf
from src.entities.Cliente import Cliente
from src.utils.validators import cpf_valido
# from marshmallow import ValidationError

def getAllClientes():
    return get_all_clientes()

def getCliente(cliente_id):
    return get_cliente_by_id(cliente_id)

def addCliente(nome: str, cpf: str, telefone: str)-> Cliente:

    if not cpf_valido(cpf):
        raise ValueError("CPF inválido.")
    
    cadastrado = get_cliente_by_cpf(cpf)
    if cadastrado:
        raise ValueError("CPF já cadastrado.")
    
    return add_cliente(nome, cpf, telefone)

def updateCliente(id: int, nome: str, cpf: str, telefone: str) -> Cliente:
    if not cpf_valido(cpf):
        raise ValueError("CPF inválido.")
    
    cadastrado = get_cliente_by_cpf(cpf)
    if cadastrado and cadastrado.id != id:
        raise ValueError("CPF já cadastrado.")
    
    return update_cliente(id=id, nome=nome, cpf=cpf, telefone=telefone)

def deleteCliente(cliente_id):
    return delete_cliente(cliente_id)