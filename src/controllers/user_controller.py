
from pydantic import EmailStr
from sqlalchemy import Update
from src.models.token_user import TokenValidation
from src.schemas.user_filter import ChangePasswordValidation
from src.services.email.create_redis import redis_create_user, get_account_after_token_correct, compare_redis_for_change_password, delete_token_from_redis_after_token
from src.services.email.code_gerator import create_token
from src.models.user import User
from src.schemas.user_filter import CreateUser, UserLogin, ChangePassword
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.services.email.email_factory import FactoryMessage
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta
import jwt
from dotenv import load_dotenv
import os
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
load_dotenv()
key = os.getenv("SECRET_KEY")
#this function checks if the email is correct, creates the hash,
# calls the function to send the email(services/emails/send_email) and store the hash in redis,
# and finally saves it in the database
#function of create Users
def user_create_redis(register: CreateUser) -> None:
    try:
        create = FactoryMessage.factory_method("create_account")
        token = create_token()
        redis_create_user(register, token)
        create.send_emails(register.email, register.nome, token)
    except Exception:
        raise HTTPException(status_code=500, detail="email get off on air")


def function_for_get_user(email: EmailStr, db: Session, token_send: str) -> None:
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
        delete_token_from_redis_after_token(email)
    except Exception:
        raise HTTPException(status_code=500, detail="server error")


#function of login users
#note for me -> after add opcional verify in two steps
def verify_login(user: UserLogin, db: Session) -> User:
    result_user = db.query(User).filter(User.email == user.email).first()
    if result_user is None or not isinstance(result_user, User):
            raise HTTPException(status_code=400, detail="email or password incorrect")
    if not pwd_context.verify(user.senha, str(result_user.password)):
        raise HTTPException(status_code=400, detail="email or password incorrect")
    return result_user



def send_change_password_function(user: ChangePassword, db: Session) -> None:
    try:
        token = create_token()
        change = FactoryMessage.factory_method("change_password")
        user_verify = db.query(User).filter(User.email == user.email).first()
        if user_verify is None:
            raise HTTPException(status_code=400, detail="email or password incorrect" )
        username = str(user_verify.name)
        change.send_emails(email_end=user.email, nome=username, token=token)
    except Exception:
        raise HTTPException(status_code=500, detail="internal server erro")


def verify_change_password(user: ChangePasswordValidation, db: Session) -> dict[str, str] | None:
    try:
        user_verify = compare_redis_for_change_password(email=user.email, token=user.token)
        pwd_hash = pwd_context.hash(user.senha)
        if user_verify:
            change = Update(User).where(User.email == user.email).values(password=pwd_hash)
            db.execute(change)
            db.commit()
            delete_token_from_redis_after_token(user.email)
            return {"message": "perfect, password changed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_jwt_acesses_token_user(id_user: int, db: Session) -> str:
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="server error NF")
    payload = {
            "sub": str(user.id),
            "name":user.name,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            "iat": datetime.now(timezone.utc),
            "type": "access",
            "role": "user"
        }
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

def create_jwt_refresh_token_user(id_user: int, db: Session) -> dict:
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="server error NF")
    payload = {
        "sub": str(user.id),
        "type": "refresh_token",
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
        "role": "user"
    }
    token = jwt.encode(payload, key, algorithm="HS256")
    return {"token": token, "dateexp":payload["exp"]}

def save_refresh_token_user(user: User, db: Session) -> str:
    token = create_jwt_refresh_token_user(user.id, db)
    try:
        refresh = TokenValidation(
            id_usuario=user.id,
            refresh_token=token["token"],
            date_expired=token["dateexp"],
        )
        db.add(refresh)
        db.commit()
        db.refresh(refresh)
        return token["token"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_acesses_jwt(token: str) -> dict[str, str] | None:
    try:
        dados = jwt.decode(token, key, algorithms=["HS256"])
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_refresh_token(token: str, db: Session) -> dict[str, str]:
    try:
        dados = jwt.decode(token, key, algorithms=["HS256"])
        refresh = db.query(TokenValidation).filter(TokenValidation.id_usuario == dados["sub"]).first()
        if refresh is None or not isinstance(refresh, TokenValidation):
            raise HTTPException(status_code=500, detail="server error NF")
        if not refresh.is_revoked:
            raise HTTPException(status_code=401, detail="token blocked", headers={"WWW-Authenticate": "Bearer"})
        return dados
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")
