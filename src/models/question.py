from src.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, CHAR, Text

class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('user.id'), nullable=False)
    statement = Column("statement", Text, nullable=False)
    response_A = Column("response A", Text, nullable=False)
    response_B = Column("response B", Text, nullable=False)
    response_C = Column("response C", Text, nullable=False)
    response_D = Column("response D",  Text, nullable=False)
    response_E = Column("response E", Text, nullable=True)
    resolution = Column("resolution", Text, nullable=False)
    correctResponse = Column("correct answer", CHAR(1), nullable=False)
    user = relationship("User", back_populates="question")