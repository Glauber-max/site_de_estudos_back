from sqlalchemy.exc import IntegrityError
from src.models import User
from src.schemas import CreateUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.services.email.send_email import send_service

#this function checks if the email is correct, creates the hash,
# calls the function to send the email(services/emails/send_email) and store the hash in redis,
# and finally saves it in the database
#function of create Users
def create_user_validation(register: CreateUser, db: Session):
    send = send_service()
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    password_hash = pwd_context.hash(register.senha)
    if "@gmail.com" in register.email:
        send.send_emails(email_end=register.email, nome=register.nome)
        new = register.model_dump()
        try:
            new_user = User(
                nome=new["nome"],
                senha=password_hash,
                email=new["email"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            db.rollback()