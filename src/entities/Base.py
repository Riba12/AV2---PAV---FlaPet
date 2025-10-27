from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy

"""SQLAlchemy: ORM - Mapeamento Objeto-Relacional 
Contém as funções de manipulação dos objetos no BD
(insert, update, delete, select)
"""
Base = declarative_base()
db = SQLAlchemy()
