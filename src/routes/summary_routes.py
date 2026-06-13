import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.conecction import get_db
from src.controllers.summary_controller import CreateSummaryFromYoutube
from src.schemas.summary_filter import SchemaCreateSummaryFromYoutube, SummaryCreate
from src.services.summary_IA.ia_factory import FactorySummary
from src.controllers.user_controller import verify_acesses_jwt
from src.models.summary import Summary
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
import json

security = HTTPBearer()
router = APIRouter()

@router.post("/summary_videos/download", status_code=201, response_model=SummaryCreate)
def summary_videos(
        video: SchemaCreateSummaryFromYoutube,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = verify_acesses_jwt(credentials)
    url_str = str(video.url)
    pytube = CreateSummaryFromYoutube()
    path = pytube.get_audio_from_youtube(url_str)
    try:
        ia = FactorySummary.factory_method("3.5")
        summary = ia.summarize(path)
    except Exception as e:
        print(f"Error first model: {e}")
        try:
            ia = FactorySummary.factory_method("2.5")
            summary = ia.summarize(path)
        except Exception as error:
            print(f"Error last model: {error}")
            raise HTTPException(status_code=503, detail="IA cant summarize this")
    try:
        dados_json = json.loads(summary)
        db_save = Summary(
            content=dados_json["content"],
            subject=dados_json["subject"],
            id_usuario=int(user["sub"])
        )
    except (json.JSONDecoder, KeyError) as error:
        print(f"Error second model: {error}")
        raise HTTPException(status_code=422, detail="the structure return summary failed ")
    try:
        os.remove(path=path)
        db.add(db_save)
        db.commit()
        db.refresh(db_save)
        return dados_json
    except Exception as error:
        print(f"Error in database store: {error}")
        raise HTTPException(status_code=500, detail="error saving in database")

@router.get(f"/summary_videos/filter", status_code=200)
def see_summary(subject: str = None, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = verify_acesses_jwt(credentials)
    summary = db.query(Summary).filter(Summary.id_usuario == user["sub"]).all()
    if not summary or isinstance(summary, Summary):
        raise HTTPException(status_code=404, detail="Summary not found")
    if subject:
        summary_list = [l for l in summary if subject.lower() in l.subject.lower()]
        return {"summary": summary_list}
    return {"summary": []}

@router.get("/summary_videos/see_all", status_code=200)
def see_all_summary(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = verify_acesses_jwt(credentials)
    summary = db.query(Summary).where(Summary.id_usuario == int(user["sub"])).all()
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return {"summary": summary}

@router.delete("/summary_videos/delete/{id_summary}", status_code=200)
def delete_summary(
        id_summary: int,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_acesses_jwt(credentials)

    try:
        summary = db.query(Summary).filter(Summary.id == id_summary).delete()
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        db.commit()
        return {"message": "summary deleted successfully"}
    except Exception as error:
        print(f"Error in database delete: {error}")
        raise HTTPException(status_code=500, detail="error deleting summary")