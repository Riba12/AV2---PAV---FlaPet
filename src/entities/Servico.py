from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from src.entities.Base import Base
import src.entities.Agendamento
class Servico(Base):
    __tablename__ = "servico"

    # Colunas
    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(255) , nullable=False)
    descricao = Column("descricao", String(255) , nullable=True)
    valor = Column("valor", DECIMAL(10, 2))
    tempo_minutos = Column("tempo_minutos", Integer)

    agendamentos = relationship("Agendamento", back_populates="servico")
