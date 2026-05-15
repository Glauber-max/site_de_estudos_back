#I will make all routes about "users",
# like: register, login, switch password and such.
from pydantic import EmailStr
from src.schemas.user_filter import CreateUser, UserLogin, ChangePassword, ChangePasswordValidation
#imports used
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src.models import User

#Create a variable router
router = APIRouter()

#router of create users, it verifies if email exists, if no, this function calls the others functions for store in redis the user
@router.post("/create_user", status_code=201)
async def register_routes(register: CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
    db_users = db.query(User).filter(User.email == register.email).first()
    if db_users:
        raise HTTPException(status_code=400, detail="email already exists")
    background_tasks.add_task(
            user_controller.user_create_redis, register=register
        )
    return {"message": "User created successfully, please verify your token in your email"}


#router for get token and email, this router calls other functions for get create user request and valid this, after add in database
@router.post("/validation_account", status_code=201)
def router_for_validation_token(email: EmailStr, token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="email already exists")
    user_controller.function_for_get_user(email=email, db=db, token_send=token)
    return {"message": "Token sent successfully, account activated"}

#this router make a login in project, now this only verify the password hash and a password send for user
@router.post("/login", status_code=200)
def login(logins: UserLogin, db: Session = Depends(get_db)):
    try:
        result_login = user_controller.verify_login(user=logins, db=db)
        return result_login
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

#this router change a password, it calls others functions for send token
@router.post("/change_passoword", status_code=200)
async def change_password(user: ChangePassword, background_tasks: BackgroundTasks , db: Session = Depends(get_db)):
    background_tasks.add_task(
        user_controller.send_change_password_function, user=user, db=db
    )
    return {"message": "if emails exists, a token will send"}

#this router valid the token and accept other password
@router.patch("/token/change_password", status_code=200)
def verify_token_for_change_password(user: ChangePasswordValidation, db: Session = Depends(get_db)):
    message = user_controller.verify_change_password(user=user, db=db)
    return message



