import re
from src.repositories.ClienteRepository import delete_cliente, update_cliente, add_cliente, get_all_clientes, get_cliente_by_id
from src.entities.Cliente import Cliente
# from marshmallow import ValidationError

def getAllClientes():
    return get_all_clientes()

def getCliente(cliente_id):
    return get_cliente_by_id(cliente_id)

# def addCliente(nome: str, cpf: str, telefone: str)-> Cliente:

#     cpf_limpo = re.sub(r'[^0-9]', '', cpf)