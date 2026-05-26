from pydantic import EmailStr
from sqlalchemy import update
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.controllers.user_controller import create_jwt_refresh_token_user
from src.models.token_user import TokenValidation
from src.schemas.user_filter import CreateUser, UserLogin, ChangePassword, ChangePasswordValidation
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src.models import User
from src.schemas.user_filter import RefreshToken

router = APIRouter()
security = HTTPBearer()


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


'''
            MAKE A CHANGE WHEN CREATE THE FRONT END

The route below needs improvements, as it only accepts one device. 
If you try to add more, it asks for login again and generates another refresh token on top. 
I should implement a device ID system to identify the user's device and create a refresh token for
each of the user's devices, thus allowing multiple devices on the same account (I should start doing 
this when creating the front end).
'''
@router.post("/login", status_code=200)
def login(logins: UserLogin, db: Session = Depends(get_db)) -> dict:
    result_login = user_controller.verify_login(user=logins, db=db)
    access_token = user_controller.create_jwt_acesses_token_user(result_login)
    refresh_exists = db.query(TokenValidation).filter(TokenValidation.id_usuario==result_login.id).first()
    if refresh_exists:
        refresh_token_update = create_jwt_refresh_token_user(result_login.id)
        updates = update(TokenValidation).where(TokenValidation.id_usuario==result_login.id).values(
            refresh_token=refresh_token_update["token"],
            date_expired=refresh_token_update["dateexp"]
        )

        db.execute(updates)
        db.commit()
        return {"access": access_token, "refresh": refresh_token_update["token"]}
    refresh_token =  user_controller.save_refresh_token_user(result_login, db)
    return {"access": access_token, "refresh": refresh_token}


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
def requirements_token(refresh_token:  RefreshToken, db: Session = Depends(get_db)) -> dict[str, dict | str]:
    dados = user_controller.verify_refresh_token(refresh_token.refresh_token, db)
    user = db.query(User).filter(User.id==dados["sub"]).first()
    if not user or not isinstance(user, User):
        raise HTTPException(status_code=401, detail="invalid refresh token")
    token = create_jwt_refresh_token_user(user.id)
    access_token = user_controller.create_jwt_acesses_token_user(user)
    updates = update(TokenValidation).where(TokenValidation.id_usuario==user.id).values(refresh_token=token)
    db.execute(updates)
    db.commit()
    return {"refresh_token": token, "access_token": access_token}

'''
In this route, I planned to do a soft delete, but due to tight deadlines at college,
I will leave it as an improvement for the next semester. For now, it is a hard delete route
to remove the user from the database along with their related records. PS: add the soft delete,
but allow the user to create the account even with their record in the database,
and allow reactivating or restoring the account.
'''
@router.delete("/delete/tables", status_code=200)
def hard_delete(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    jwt = credentials.credentials.strip()
    user = user_controller.verify_acesses_jwt(jwt)
    user_for_delete = db.query(User).filter(User.id == user["sub"]).first()
    if user_for_delete is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    try:
        db.delete(user_for_delete)
        db.commit()
        return {"message": "user deleted"}
    except Exception as e:
        print(f"account cant be deleted: {e}")
        raise HTTPException(status_code=500, detail="cant be deleted")

@router.post("/logout", status_code=200)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    jwt = credentials.credentials.strip()
    user = user_controller.verify_acesses_jwt(jwt)
    refresh = db.query(TokenValidation).filter(TokenValidation.id_usuario == user["sub"]).first()
    if not refresh:
        raise HTTPException(status_code=404, detail="Session not found.")
    db.delete(refresh)
    db.commit()
    return {"message": "user logged out"}

@router.get("/obter/usuario", status_code=200)
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    jwt = credentials.credentials.strip()
    user_jwt = user_controller.verify_acesses_jwt(jwt)
    user = db.query(User).filter(User.id == user_jwt["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account not found.")
    return {"user": user}