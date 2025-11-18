from src.entities.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Raca(Base):
    __tablename__ = "Raca"

    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(100) , nullable=False)

    # FK
    especie_id = Column("especie_id", Integer, ForeignKey("Especie.id", ondelete="CASCADE"), nullable=False)


    especie = relationship("Especie", back_populates="racas")
    animais = relationship("Animal", back_populates="raca")