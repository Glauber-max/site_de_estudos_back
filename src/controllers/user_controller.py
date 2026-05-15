from pydantic import EmailStr
from sqlalchemy import Update
from src.schemas.user_filter import ChangePasswordValidation
from src.services.email.create_redis import redis_create_user, get_account_after_token_correct, compare_redis_for_change_password, delete_account_after_token
from src.services.email.code_gerator import create_token
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
        token = create_token()
        redis_create_user(register, token)
        create.send_emails(register.email, register.nome, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def function_for_get_user(email: EmailStr, db: Session, token_send: str):
    try:
        json_user = get_account_after_token_correct(email)
        if json_user["token"] != token_send:
            raise HTTPException(status_code=400, detail="token incorrect")
        pwd_hash = pwd_context.hash(json_user["password"])
        save_user = User(
            name=json_user["name"],
            password=pwd_hash,
            email=json_user["email"],
        )
        db.add(save_user)
        db.commit()
        db.refresh(save_user)
        delete_account_after_token(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#function of login users
#note for me -> after add opcional verify in two steps
def verify_login(user: UserLogin, db: Session):
    result_user = db.query(User).filter(User.email == user.email).first()
    if result_user is None:
            raise HTTPException(status_code=400, detail="email or password incorrect")
    if not pwd_context.verify(user.senha, str(result_user.password)):
        raise HTTPException(status_code=400, detail="email or password incorrect")
    return {"message": "credentials correct, login successful"}

def send_change_password_function(user: ChangePassword, db: Session):
    token = create_token()
    change = FactoryMessage.factory_method("change_password")
    try:
        user_verify = db.query(User).filter(User.email == user.email).first()
        if not user_verify:
            raise HTTPException(status_code=400, detail="if email exists, a token will send")
        change.send_emails(email_end=user.email, nome=user_verify.name, token=token)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def verify_change_password(user: ChangePasswordValidation, db: Session):
    try:
        user_verify = compare_redis_for_change_password(email=user.email, token=user.token)
        pwd_hash = pwd_context.hash(user.senha)
        if user_verify:
            change = Update(User).where(User.email == user.email).values(password=pwd_hash)
            db.execute(change)
            db.commit()
            delete_account_after_token(user.email)
            return {"message": "perfect, password changed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

