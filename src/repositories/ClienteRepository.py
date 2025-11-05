from src.entities import Cliente
from src.entities.Base import db

def get_all_clientes() :
    """
    Get all clientes stored in the database.

    Returns:
        clientes (Cliente) -- contains all clientes registered.
    """
    clientes = db.session.query(Cliente).all()
    
    return clientes

def get_cliente_by_id(cliente_id: int) -> Cliente:
    """
    Get one cliente stored in the database.

    Returns:
        cliente (Cliente) -- find one cliente registered.
    """
    # SELECT * FROM CLIENTE WHERE id=cliente_id
    cliente = db.session.query(Cliente).get(cliente_id)
    
    return cliente

def add_cliente(id: int, nome: str, cpf: str, telefone: str) -> Cliente:
    cliente = Cliente(id=id, nome=nome, cpf=cpf, telefone=telefone)
    
    # INSERT INTO CLIENTE values (id, nome, email)
    db.session.add(cliente)

    # Confirma a execução
    db.session.commit()

    return cliente

def update_cliente(id: int, nome: str, cpf: str, telefone: str) -> Cliente:
    """
    Update a Cliente in the database.

    Returns:
        cliente (Cliente) -- updated cliente.
    """
    # Verifica se o cliente existe
    cliente = db.session.query(Cliente).get(id)

    if(not cliente):
        raise Exception
    
    cliente.nome = nome
    cliente.cpf = cpf
    cliente.telefone = telefone

    db.session.commit()

    return cliente

def delete_cliente(cliente_id) -> Cliente:
    """
    Delete one cliente stored in the database.

    Returns:
        cliente (Cliente) -- deleted cliente.
    """
    # Verifica se o cliente existe
    cliente = db.session.query(Cliente).get(cliente_id)

    if(not cliente):
        return None
    
    db.session.delete(cliente)
    db.session.commit()

    return cliente