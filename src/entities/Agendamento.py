from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.entities.Base import Base
import enum

class StatusAgendamento(enum.Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"
    CONCLUIDO = "CONCLUIDO"


class Agendamento(Base):
    __tablename__ = "Agendamento"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    data_hora = Column("data_hora", DateTime)
    status = Column(enum.Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE, nullable=False)

    # FK's
    servico_id = Column("servico_id", Integer, ForeignKey("Servico.id", ondelete="CASCADE"), nullable=False)
    animal_id = Column("animal_id", Integer, ForeignKey("Animal.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    animal = relationship("Animal", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")