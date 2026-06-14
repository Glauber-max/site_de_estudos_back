import json
from turtledemo.penrose import star

from soupsieve.util import lower
from sqlalchemy import update
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.services.question_IA.factory_ia_question import FactoryQuestionIA
from src.models.question import Question
from src.controllers.user_controller import verify_acesses_jwt
from src.database.conecction import get_db
from src.schemas.question_filter import CreateQuestion, QuestionRequest
import logging
logger = logging.getLogger(__name__)
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
        logger.error("error in save question", error)
        raise HTTPException(status_code=500, detail="Error in saving question")

@router.post("/create/question/ia", status_code=201)
def create_question_ia(
        request_question: QuestionRequest,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = verify_acesses_jwt(credentials)
    models = ["2.5", "3.5"]
    question = None
    for model in models:
        try:
            engine = FactoryQuestionIA.make_question(model)
            question = engine.make_question(
                summary=request_question.summary,
                number_of_questions=request_question.number_of_questions
            )
            break
        except Exception as error:
            logger.warning("first model failed", error)

    if not question:
        logger.error("two models failed in create question")
        raise HTTPException(status_code=500, detail="Error in creating question")
    try:
        question_json = json.loads(question)
        list_of_questions = question_json.get("questions", [])
        for question in list_of_questions:
            db_save =  Question(**question, id_usuario=int(user["sub"]))
            db.add(db_save)
        db.commit()
        return list_of_questions
    except Exception as errors:
        db.rollback()
        logger.error("error in save question", errors)
        raise HTTPException(status_code=500, detail="Error in saving question")

@router.patch("/update/question/{question_id}", status_code=201)
def update_question(
        question_id: int,
        question: CreateQuestion,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_acesses_jwt(credentials)
    question_switch = question.model_dump(exclude_unset=True)
    if not question_switch:
        raise HTTPException(status_code=404, detail="Error in patch question")
    try:
        db.execute(update(Question).where(Question.id == question_id).values(**question_switch))
        db.commit()
        return {"message": "questions successfully updated"}
    except Exception as error:
        db.rollback()
        logger.error("error in update question", error)
        raise HTTPException(status_code=500, detail="Error in updating question")

@router.delete("/delete/question/{question_id}", status_code=204)
def delete_question(
        question_id: int,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = verify_acesses_jwt(credentials)
    question = db.query(Question).filter(Question.id == question_id, Question.id_usuario == int(user["sub"])).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Error in delete question")
    db.delete(question)
    return

@router.get("/questions/get_all", status_code=200)
def get_all_questions(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = verify_acesses_jwt(credentials)
    db_questions = db.query(Question).filter(Question.id_usuario == user["sub"]).limit(100).all()
    if db_questions is None:
        raise HTTPException(status_code=404, detail="Error in get all questions")
    return db_questions

@router.get("/questions/filter", status_code=200)
def filter_questions(
        statement: str = None,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = verify_acesses_jwt(credentials)
    if statement:
        list_of_questions = db.query(Question).filter(
            Question.id_usuario == int(user["sub"]),
            Question.statement.ilike(f"%{statement}%")
        ).all()
        return list_of_questions

    return {"message": []}