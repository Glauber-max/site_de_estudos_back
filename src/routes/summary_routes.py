#this routes is only for summary
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.conecction import get_db
from src.schemas.summary_filter import CreateSummaryFromYoutube
from src.controllers.summary_controller import get_audio_from_youtube



router = APIRouter()
@router.post("/summary_videos/download")
def summary_videos(video: CreateSummaryFromYoutube, db: Session = Depends(get_db)):
    url_str = str(video.url)
    yt_audio = get_audio_from_youtube(url_str)


