from src.controllers.ClienteController import ClienteList, ClienteItem
from src.controllers.AnimalController import AnimalList, AnimalItem
from src.controllers.AgendamentoController import AgendamentoList, AgendamentoItem
from src.controllers.EspecieController import EspecieList, EspecieItem
from src.controllers.RacaController import RacaList, RacaItem
from src.controllers.ServicoController import ServicoList, ServicoItem

def initialize_endpoints(api):

    #cliente endpoints
    api.add_resource(ClienteList, "/clientes")
    api.add_resource(ClienteItem, "/clientes/<int:cliente_id>")

    #animal endpoints
    api.add_resource(AnimalList, "/animais")
    api.add_resource(AnimalItem, "/animais/<int:animal_id>")

    #agendamento endpoints
    api.add_resource(AgendamentoList, "/agendamentos")
    api.add_resource(AgendamentoItem, "/agendamentos/<int:agendamento_id>")

    #especie endpoints
    api.add_resource(EspecieList, "/especies")
    api.add_resource(EspecieItem, "/especies/<int:especie_id>")

    #raca endpoints
    api.add_resource(RacaList, "/racas")
    api.add_resource(RacaItem, "/racas/<int:raca_id>")

    #servico endpoints
    api.add_resource(ServicoList, "/servicos")
    api.add_resource(ServicoItem, "/servicos/<int:servico_id>")