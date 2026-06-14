from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models import Question
from src.controllers.user_controller import verify_acesses_jwt
from src.database.conecction import get_db
from src.schemas.question_filter import CreateQuestion

router = APIRouter()
security = HTTPBearer()
@router.post("/create/question", status_code=201)
def create_question(
        question: CreateQuestion,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = verify_acesses_jwt(credentials)
    save_question = question.model_dump()
    try:
        new_question = Question(**save_question, id_usuario=int(user["sub"]))
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
    except Exception as error:
        db.rollback()
        print("error in save question", error)
        raise HTTPException(status_code=500, detail="Error in saving question")


