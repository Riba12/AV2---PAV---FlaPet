from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.entities.Base import Base

class Animal(Base):
    __tablename__ = "Animal"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(255) , nullable=False)
    especie = Column("especie", String(100) , nullable=False)
    raca = Column("raca", String(100))

    # FK's
    cliente_id = Column("cliente_id", Integer, ForeignKey("Cliente.id", ondelete="CASCADE"), nullable=False)

    cliente = relationship("Cliente", back_populates="animais")
    agendamentos = relationship("Agendamento", back_populates="animal")