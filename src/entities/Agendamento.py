from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.entities.Base import Base

class Agendamento(Base):
    __tablename__ = "Agendamento"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    data_hora = Column("data_hora", DateTime)
    status = Column("status", String(100))

    #FK's
    servico_id = Column("servico_id", Integer, ForeignKey("Servico.id", ondelete="CASCADE"), nullable=False)
    animal_id = Column("animal_id", Integer, ForeignKey("Animal.id", ondelete="CASCADE"), nullable=False)

    animal = relationship("Animal", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")