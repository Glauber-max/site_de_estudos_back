from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True, autoincrement=True, nullable=False)
    nome = Column("name", String(40), nullable=False)
    senha = Column("password", String(255), nullable=False)
    email = Column("email", String(100), nullable=False)
    anotacoes = relationship("Notes", back_populates="users")
    agenda = relationship( "Agenda", back_populates="users")
    resumo = relationship("Summary", back_populates="users")
    questoes = relationship("Questao", back_populates="users")