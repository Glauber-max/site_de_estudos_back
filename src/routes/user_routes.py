#I will make all routes about "users",
# like: register, login, switch password and such.

#imports used
from src.controllers import user_controller
from fastapi import APIRouter, Depends
from src.database.conecction import  get_db
from sqlalchemy.orm import Session
from src import schemas as sch

#Create a variable router
router = APIRouter()

#router of create users and return users of /schemas
@router.post("/create_user", response_model= sch.UserResponse)
def register_routes(register: sch.CreateUser, db: Session = Depends(get_db)):
    new_user = user_controller.create_user_validation(db=db, register=register)
    return new_user


