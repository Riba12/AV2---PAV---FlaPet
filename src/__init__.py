from flask import Flask
from flask_restful import Api
# from src.routes.endpoints import initialize_endpoints
from src.entities.Base import db

# Função que cria a API
def create_app() -> Flask:
    # Definindo qual é o banco de dados
    app = Flask(__name__)
    # mudar para string do banco de verdade, usar .env 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/academico'

    db.init_app(app)

    # Flask API
    api = Api(app, prefix="/academico")
    # initialize_endpoints(api)

    return app