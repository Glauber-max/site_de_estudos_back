from sqlalchemy.exc import IntegrityError

from src.models import User
from src.schemas import CreateUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

#function of create Users
def create_user_validation(register: CreateUser, db: Session) -> User:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    password_hash = pwd_context.hash(register.senha)
    new = register.model_dump()
    if "@gmail.com" in register.email.lower():
        try:
            new_user = User(
                nome=new["nome"],
                senha=password_hash,
                email=new["email"],
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=str("error, email already exists"))
    else:
        raise HTTPException(status_code=400, detail={"message": "email not suported or error write email"})