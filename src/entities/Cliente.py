from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.entities.Base import Base
import src.entities.Animal

class Cliente(Base):
    __tablename__ = "cliente"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(255) , nullable=False)
    cpf = Column("cpf", String(14) , nullable=False, unique=True)
    telefone = Column("telefone", String(20) , nullable=False)

    animais = relationship("Animal", back_populates="cliente")