from main import app
from src.entities.Base import db
from src.entities.Agendamento import Agendamento
from src.entities.Animal import Animal
from src.entities.Cliente import Cliente
from src.entities.Servico import Servico
from src.entities.Especie import Especie
from src.entities.Raca import Raca

with app.app_context():
    db.create_all()

print("Banco de dados e tabelas criados com sucesso!")