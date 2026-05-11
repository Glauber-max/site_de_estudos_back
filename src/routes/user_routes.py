#I will make all routes about "users",
# like: register, login, switch password and such.

#imports used
from src.controllers import user_controller
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src import schemas as sch
from src.services.email.create_redis import compare_redis

#Create a variable router
router = APIRouter()

#router of create users and return users of /schemas
@router.post("/create_user")
async def register_routes(register: sch.CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
    background_tasks.add_task(
        user_controller.create_user_validation, db=db, register=register
    )
    return {"message": "User created successfully"}

@router.post("/send_token")
def send_token(token: str, email: str):
    response = compare_redis(code_writed=token, email_end=email)
    if response:
        return {"message": "Token sent successfully, account activated"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect token")


