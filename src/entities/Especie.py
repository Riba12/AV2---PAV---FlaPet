from src.entities.Base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Especie(Base):
    __tablename__ = "Especie"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(100) , nullable=False, unique=True)

    animais = relationship("Animal", back_populates="especie")

    racas = relationship("Raca", back_populates="especie")