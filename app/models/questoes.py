from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, CHAR, Text

class Questao(Base):
    __tablename__ = "questao"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    enunciado = Column("enunciado", Text, nullable=False)
    resposta_A = Column("resposta A", Text, nullable=False)
    resposta_B = Column("resposta B", Text, nullable=False)
    resposta_C = Column("resposta C", Text, nullable=False)
    resposta_D = Column("resposta D",  Text, nullable=False)
    resposta_E = Column("resposta E", Text, nullable=True)
    resolucao = Column("resolução", Text, nullable=False)
    resposta_correta = Column("resposta correta", CHAR(1), nullable=False)
    usuario = relationship("Usuario", back_populates="questao")