#I will make all routes about "users",
# like: register, login, switch password and such.
from src.schemas.user_filter import CreateUser, UserLogin
#imports used
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src.services.email.create_redis import compare_redis
from src.models import User

#Create a variable router
router = APIRouter()

#router of create users, it verifies if email exists, if not,he used a function in controllers
@router.post("/create_user", status_code=201)
async def register_routes(register: CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
    db_users = db.query(User).filter(User.email == register.email).first()
    if db_users:
        raise HTTPException(status_code=400, detail="email already exists")
    background_tasks.add_task(
            user_controller.create_user_validation, db=db, register=register
        )
    return {"message": "User created successfully, please verify your token in your email"}

#it functions verify if token are correct
@router.post("/send_token", status_code=200)
def verifies_token(email: str, token: str, dbs: Session = Depends(get_db)):
    response = compare_redis(code_write=token, email_end=email)
    if not response:
        raise HTTPException(status_code=400, detail="incorrect token")
    try:
        db_users = dbs.query(User).filter(User.email == email).first()
        db_users.active = True
        dbs.commit()
        dbs.refresh(db_users)
        return {"message": "Token sent successfully, account activated"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/login", status_code=200)
def login(logins: UserLogin, db: Session = Depends(get_db)):
    try:
        result_login = user_controller.verify_login(user=logins, db=db)
        return result_login
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

