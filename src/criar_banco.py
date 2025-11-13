from main import app
from src.entities.Base import db
from src.entities.Agendamento import Agendamento
from src.entities.Animal import Animal
from src.entities.Cliente import Cliente
from src.entities.Servico import Servico

with app.app_context():
    db.create_all()

print("Banco de dados e tabelas criados com sucesso!")