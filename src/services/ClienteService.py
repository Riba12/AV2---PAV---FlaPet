from src.entities import Cliente
from src.repositories.ClienteRepository import delete_cliente, update_cliente, add_cliente, get_all_clientes, get_cliente_by_id
from marshmallow import ValidationError

def getAllClientes():
    return get_all_clientes()