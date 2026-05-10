
from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

class Anotacoes(Base):
    __tablename__ = 'anotacoes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False, index=True)
    titulo = Column("titulo", String(100), nullable=False)
    descricao = Column("Descricao", Text, nullable=False)
    usuario = relationship("Usuario", back_populates="anotacoes")