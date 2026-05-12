from src.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Boolean, Text


class Agenda(Base):
    __tablename__ = 'agenda'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey("user.id"), nullable=False)
    data_inicio = Column("start", DATETIME, nullable=False)
    data_final = Column("end", DATETIME, nullable=False)
    titulo = Column("title", String(100), nullable=False)
    descricao = Column("description", Text, nullable=False)
    cor = Column("color", String(7), nullable=False)
    concluido = Column("completed", Boolean, nullable=False, default=False)
    user = relationship("User", back_populates="agenda")