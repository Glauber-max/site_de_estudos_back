
from app.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    title = Column("title", String(100), nullable=False)
    description = Column("description", Text, nullable=False)
    user = relationship("User", back_populates="notes")