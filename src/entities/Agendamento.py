from sqlalchemy import Column, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from src.entities.Base import Base
import src.entities.Servico
import src.entities.Animal
import enum

class StatusAgendamento(enum.Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"
    CONCLUIDO = "CONCLUIDO"


class Agendamento(Base):
    __tablename__ = "agendamento"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    data_hora = Column("data_hora", DateTime)
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE, nullable=False)

    # FK's
    servico_id = Column("servico_id", Integer, ForeignKey("servico.id", ondelete="CASCADE"), nullable=False)
    animal_id = Column("animal_id", Integer, ForeignKey("animal.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    animal = relationship("Animal", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")