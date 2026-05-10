from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Text


class Resumo(Base):
    __tablename__ = 'resumo'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    conteudo = Column("conteudo", Text, nullable=False)
    assunto = Column("assunto", Text, nullable=False)
    usuario = relationship("Usuario", back_populates="resumo")