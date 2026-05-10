from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Text


class Summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column("content", Text, nullable=False)
    subject = Column("subject", Text, nullable=False)
    user = relationship("User", back_populates="summary")