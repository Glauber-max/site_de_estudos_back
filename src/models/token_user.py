from src.database.conecction import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean

class TokenValidation(Base):
    __tablename__ = 'token_validation'
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    id_usuario = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    refresh_token = Column("refresh_token", Text, nullable=False)
    device_id = Column("device id", Integer, nullable=True, index=True, default=None)
    date_expired = Column("date_expired", DateTime, nullable=False)
    is_revoked = Column("is_revoked", Boolean, nullable=False, default=False)
    user = relationship("User", back_populates="token_validation")