from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Boolean, Text


class Agenda(Base):
    __tablename__ = 'agenda'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    data_inicio = Column("inicio", DATETIME, nullable=False)
    data_final = Column("fim", DATETIME, nullable=False)
    titulo = Column("titulo", String(100), nullable=False)
    descricao = Column("descricao", Text, nullable=False)
    cor = Column("cor", String(7), nullable=False)
    concluido = Column("concluido", Boolean, nullable=False)
    usuario = relationship("Usuario", back_populates="agenda")