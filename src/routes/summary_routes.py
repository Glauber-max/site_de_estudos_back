#this routes is only for summary
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.conecction import get_db
from src.controllers.summary_controller import CreateSummaryFromYoutube
from src.schemas.summary_filter import SchemaCreateSummaryFromYoutube
from src.services.summary_IA.ia_factory import FactorySummary
from src.controllers.user_controller import verify_acesses_jwt
from src.models.summary import Summary
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()
router = APIRouter()

@router.post("/summary_videos/download")
def summary_videos(
        video: SchemaCreateSummaryFromYoutube,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token_string = credentials.credentials.strip()
    user = verify_acesses_jwt(token_string)

    url_str = str(video.url)
    ia = FactorySummary.factory_method("flash")
    pytube = CreateSummaryFromYoutube()
    path = pytube.get_audio_from_youtube(url_str)
    text_archive = pytube.get_transcription_from_archive(path)
    try:
        summary = ia.summarize(text_archive)
    except Exception:
        ia = FactorySummary.factory_method("gemma")
        summary = ia.summarize(text_archive)
    db_save = Summary(
        content=summary.get("content"), #erro aq
        subject=summary.get("subject"),
        id_usuario=int(user["sub"])
    )
    db.add(db_save)
    db.commit()
    db.refresh(db_save)
    return {"summary": summary}



