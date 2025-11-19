from src.controllers.ClienteController import ClienteList
from src.controllers.AnimalController import AnimalList

def initialize_endpoints(api):

    #cliente endpoints
    api.add_resource(ClienteList, "/clientes")

    #animal endpoints
    api.add_resource(AnimalList, "/animais")