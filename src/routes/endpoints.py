from src.controllers.ClienteController import ClienteList

def initialize_endpoints(api):
    api.add_resource(ClienteList, "/clientes")