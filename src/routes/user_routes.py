#I will make all routes about "users",
# like: register, login, switch password and such.

#imports used
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src import schemas as sch
from src.services.email.create_redis import compare_redis
from src.models import User

#Create a variable router
router = APIRouter()

#router of create users and return users of /schemas
@router.post("/create_user")
async def register_routes(register: sch.CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
    db_users = db.query(User).filter(User.email == register.email).first()
    if db_users:
        raise HTTPException(status_code=400, detail="email already exists")
    else:
        background_tasks.add_task(
            user_controller.create_user_validation, db=db, register=register
        )
    return {"message": "User created successfully, please verify your token in your email"}

@router.post("/send_token")
def send_token(email: str, token: str, db: Session = Depends(get_db)):
    response = compare_redis(code_writed=token, email_end=email)
    if response:
        db_users = db.query(User).filter(User.email == email).first()
        if db_users:
            db_users.active = True
            db.commit()
            db.refresh(db_users)
        return {"message": "Token sent successfully, account activated"}
    raise HTTPException(status_code=400, detail="incorrect token")