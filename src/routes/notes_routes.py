from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.notes_filter import WriteNote, UpdateNote
from src.database.conecction import  get_db
from src.models.notes import Notes
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.controllers import user_controller
from sqlalchemy import update
router = APIRouter()
security = HTTPBearer()

@router.post("/write" , status_code=201)
def write_note(note: WriteNote, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials= Depends(security)):
    user = user_controller.verify_acesses_jwt(credentials)
    note_write = Notes(
        user_id=int(user["sub"]),
        title=note.title,
        description=note.description,
    )
    try:
        db.add(note_write)
        db.commit()
        db.refresh(note_write)
        return {"message": "Note successfully created"}
    except Exception as error:
        db.rollback()
        print(f"Error in database store: {error}")
        raise HTTPException(status_code=500, detail="server are error in store")

@router.get("/get_note_all", status_code=200)
def get_notes(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = user_controller.verify_acesses_jwt(credentials)
    notes = db.query(Notes).filter(Notes.user_id == int(user["sub"])).all()
    if notes is None:
        raise HTTPException(status_code=404, detail="user not exist")
    return {"notes": notes}

@router.get("/get_note/filter", status_code=200)
def get_filter_notes(title = None, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = user_controller.verify_acesses_jwt(credentials)
    notes = db.query(Notes).filter(Notes.user_id == int(user["sub"])).all()
    if notes is None:
        raise HTTPException(status_code=404, detail="user not exist")
    if title:
        notes_list = [l for l in notes if title.lower() in l.title.lower()]
        return {"notes": notes_list}
    return {"notes": []}

@router.delete("/delete_note/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_controller.verify_acesses_jwt(credentials)
    note = db.query(Notes).filter(Notes.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="note not exist")
    try:
        db.delete(note)
        db.commit()
        return None
    except Exception as error:
        print(f"Error in database delete: {error}")
        raise HTTPException(status_code=500, detail="server are error in delete any")

@router.patch("/update_note/{note_id}", status_code=200)
def update_notes(note_id: int,
                 schema_note: UpdateNote,
                 db: Session = Depends(get_db),
                 credentials: HTTPAuthorizationCredentials = Depends(security)
            ):
    user_controller.verify_acesses_jwt(credentials)
    note_switch = schema_note.model_dump(exclude_unset=True)
    if note_switch is None:
        raise HTTPException(status_code=404, detail="note not exist")
    try:
        db.execute(update(Notes).where(Notes.id == note_id).values(**note_switch))
        db.commit()
        return {"message": "Note successfully updated"}
    except Exception as error:
        print(f"Error in database update: {error}")
        raise HTTPException(status_code=500, detail="server are error in update any")