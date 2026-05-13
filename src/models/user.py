from src.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
#so i only define the tables using relationship for better experience in consult, and Base for create tables with python code
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,index=True, autoincrement=True, nullable=False)
    nome = Column("name", String(40), nullable=False)
    senha = Column("password", String(255), nullable=False)
    email = Column("email", String(100), nullable=False, index=True)
    notes = relationship("Notes", back_populates="user")
    agenda = relationship( "Agenda", back_populates="user")
    summary = relationship("Summary", back_populates="user")
    question = relationship("Question", back_populates="user")