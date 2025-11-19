from src.controllers.ClienteController import ClienteList
from src.controllers.AnimalController import AnimalList
from src.controllers.AgendamentoController import AgendamentoList
from src.controllers.EspecieController import EspecieList
from src.controllers.RacaController import RacaList 
from src.controllers.ServicoController import ServicoList

def initialize_endpoints(api):

    #cliente endpoints
    api.add_resource(ClienteList, "/clientes")

    #animal endpoints
    api.add_resource(AnimalList, "/animais")

    #agendamento endpoints
    api.add_resource(AgendamentoList, "/agendamentos")

    #especie endpoints
    api.add_resource(EspecieList, "/especies")

    #raca endpoints
    api.add_resource(RacaList, "/racas")

    #servico endpoints
    api.add_resource(ServicoList, "/servicos")