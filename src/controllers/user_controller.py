import json
from pydantic import EmailStr
from sqlalchemy import Update
from src.schemas.user_filter import ChangePasswordValidation
from src.services.email.create_redis import compare_redis
from src.services.email.create_redis import get_account_after_token_correct
from src.services.email.create_redis import redis_create_user
from src.models import User
from src.schemas.user_filter import CreateUser, UserLogin, ChangePassword
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.services.email.factory_method_ import FactoryMessage
from fastapi.exceptions import HTTPException
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
#this function checks if the email is correct, creates the hash,
# calls the function to send the email(services/emails/send_email) and store the hash in redis,
# and finally saves it in the database
#function of create Users
def user_create_redis(register: CreateUser) -> None:
    create = FactoryMessage.factory_method("create_account")
    try:
        redis_create_user(register)
        create.send_emails(register.email, register.nome)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def function_for_get_user(email: EmailStr, db: Session):
    try:
        user = get_account_after_token_correct(email)
        json_user = json.loads(user)
        pwd_hash = pwd_context.hash(json_user["password"])
        save_user = User(
            nome=json_user["name"],
            senha=pwd_hash,
            email=json_user["email"],
        )
        db.add(save_user)
        db.commit()
        db.refresh(save_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#function of login users
#note for me -> after add opcional verify in two steps
def verify_login(user: UserLogin, db: Session):
    result_user = db.query(User).filter(User.email == user.email).first()
    if result_user is None:
            raise HTTPException(status_code=400, detail="email or password incorrect")
    if not pwd_context.verify(user.senha, str(result_user.senha)):
            raise HTTPException(status_code=400, detail="email or password incorrect")
    return {"message": "credentials correct, login successful"}

def send_change_password_function(user: ChangePassword, db: Session):
    change = FactoryMessage.factory_method("change_password")
    try:
        user_verify = db.query(User).filter(User.email == user.email).first()
        if user_verify is None:
            raise HTTPException(status_code=400, detail="email or password incorrect")
        change.send_emails(email_end=user.email, nome=user.nome)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_change_password(user: ChangePasswordValidation, token, db: Session):
    try:
        user_verify = compare_redis(email_end=user.email, code_write=token)
        pwd_hash = pwd_context.hash(user.senha)
        if user_verify:
            change = Update(User).where(User.email == user.email).values(password=pwd_hash)
            db.execute(change)
            db.commit()
            return {"message": "perfect, password changed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

