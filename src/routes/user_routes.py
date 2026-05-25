
from pydantic import EmailStr
from src.schemas.user_filter import CreateUser, UserLogin, ChangePassword, ChangePasswordValidation
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src.models import User
from src.schemas.user_filter import RefreshToken

router = APIRouter()


@router.post("/create_user", status_code=202)
async def register_routes(register: CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> dict[str, str]:
    db_users = db.query(User).filter(User.email == register.email).first()
    if db_users:
        raise HTTPException(status_code=409, detail="email already exists")
    background_tasks.add_task(
            user_controller.user_create_redis, register=register
        )
    return {"message": "User created successfully, please verify your token in your email"}



@router.post("/validation_account", status_code=200)
def router_for_validation_token(email: EmailStr, token: str, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=409, detail="email already exists")
    user_controller.function_for_get_user(email=email, db=db, token_send=token)
    return {"message": "Token sent successfully, account activated"}


@router.post("/login", status_code=200)
def login(logins: UserLogin, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        result_login = user_controller.verify_login(user=logins, db=db)
        access_token = user_controller.create_jwt_acesses_token_user(result_login.id, db)
        refresh_token =  user_controller.save_refresh_token_user(result_login, db)
        return {"access": access_token, "refresh": refresh_token}
    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))


@router.post("/change_passoword", status_code=200)
async def change_password(user: ChangePassword, background_tasks: BackgroundTasks , db: Session = Depends(get_db)) -> dict[str, str]:
    background_tasks.add_task(
        user_controller.send_change_password_function, user=user, db=db
    )
    return {"message": "if emails exists, a token will be send"}


@router.patch("/token/change_password", status_code=200)
def verify_token_for_change_password(user: ChangePasswordValidation, db: Session = Depends(get_db)) -> dict[str, str] | None:
    verify_exists = db.query(User).filter(User.email==user.email).first()
    if not verify_exists:
        raise HTTPException(status_code=404, detail="Account not found. make a sing-up")
    message = user_controller.verify_change_password(user=user, db=db)
    return message

@router.post("/required/acesses_token", status_code=200)
def requirements_token(refresh_token:  RefreshToken, db: Session = Depends(get_db)) -> dict[str, str]:
    dados = user_controller.verify_refresh_token(refresh_token.refresh_token, db)
    user = db.query(User).filter(User.id==dados["sub"]).first()
    if not user or not isinstance(user, User):
        raise HTTPException(status_code=401, detail="invalid refresh token")
    token_new = user_controller.save_refresh_token_user(user, db)
    return {"refreash token": token_new}



