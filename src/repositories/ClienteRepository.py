from src.entities.Cliente import Cliente
from src.entities.Base import db

def get_all_clientes() :
    """
    Get all clientes stored in the database.

    Returns:
        clientes (Cliente) -- contains all clientes registered.
    """
    #SELECT * FROM CLIENTE
    print("antes query")
    clientes = db.session.query(Cliente).all()
    print("depois query")
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

def get_cliente_by_cpf(cpf: str) -> Cliente:
    """
    Get one cliente stored in the database by CPF.

    Returns:
        cliente (Cliente) -- find one cliente registered.
    """
    # SELECT * FROM CLIENTE WHERE cpf=cpf
    cliente = db.session.query(Cliente).filter_by(cpf=cpf).first()
    
    return cliente

def add_cliente(nome: str, cpf: str, telefone: str) -> Cliente:
    """
    Insert a Cliente in the database.
    Returns:
        cliente (Cliente) -- inserted cliente.
    """
    cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
    
    # INSERT INTO CLIENTE values (id, nome, cpf, telefone)
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
    # SELECT * FROM CLIENTE WHERE id=cliente_id
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
    # SELECT * FROM CLIENTE WHERE id=cliente_id
    cliente = db.session.query(Cliente).get(cliente_id)

    if(not cliente):
        return None
    
    db.session.delete(cliente)
    db.session.commit()

    return cliente