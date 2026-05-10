from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True,index=True, autoincrement=True, nullable=False)
    nome = Column("nome", String(40), nullable=False)
    senha = Column("senha", String(255), nullable=False)
    email = Column("email", String(100), nullable=False)
    anotacoes = relationship("Anotacoes", back_populates="usuario")
    agenda = relationship("Agenda", back_populates="usuario")
    resumo = relationship("Resumo", back_populates="usuario")
    questoes = relationship("Questao", back_populates="usuario")