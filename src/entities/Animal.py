from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.entities.Base import Base
import src.entities.Agendamento
import src.entities.Animal
import src.entities.Especie
import src.entities.Raca

class Animal(Base):
    __tablename__ = "animal"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(255) , nullable=False)

    # FK's
    cliente_id = Column("cliente_id", Integer, ForeignKey("cliente.id", ondelete="CASCADE"), nullable=False)

    especie_id = Column("especie_id", Integer, ForeignKey("especie.id", ondelete="CASCADE"), nullable=False)
    raca_id = Column("raca_id", Integer, ForeignKey("raca.id", ondelete="CASCADE"), nullable=False)

    cliente = relationship("Cliente", back_populates="animais")
    agendamentos = relationship("Agendamento", back_populates="animal")

    especie = relationship("Especie", back_populates="animais")
    raca = relationship("Raca", back_populates="animais")