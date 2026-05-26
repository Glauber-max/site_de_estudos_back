from src.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,index=True, autoincrement=True, nullable=False)
    name = Column("name", String(40), nullable=False)
    password = Column("password", String(255), nullable=False)
    email = Column("email", String(100), nullable=False, index=True)
    notes = relationship("Notes", back_populates="user", cascade="all, delete-orphan")
    agenda = relationship( "Agenda", back_populates="user", cascade="all, delete-orphan")
    summary = relationship("Summary", back_populates="user", cascade="all, delete-orphan")
    question = relationship("Question", back_populates="user", cascade="all, delete-orphan")
    token_validation = relationship("TokenValidation", back_populates="user", cascade="all, delete-orphan")