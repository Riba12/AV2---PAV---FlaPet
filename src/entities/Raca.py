from src.entities.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import src.entities.Animal
import src.entities.Especie

class Raca(Base):
    __tablename__ = "raca"

    id = Column("id", Integer , primary_key=True)
    nome = Column("nome", String(100) , nullable=False)

    # FK
    especie_id = Column("especie_id", Integer, ForeignKey("especie.id", ondelete="CASCADE"), nullable=False)


    especie = relationship("Especie", back_populates="racas")
    animais = relationship("Animal", back_populates="raca")