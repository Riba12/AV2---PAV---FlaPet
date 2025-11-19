from src.entities.Base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import src.entities.Animal
import src.entities.Raca

class Especie(Base):
    __tablename__ = "especie"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(100) , nullable=False, unique=True)

    animais = relationship("Animal", back_populates="especie")

    racas = relationship("Raca", back_populates="especie")