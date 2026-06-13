from pydantic import BaseModel

class WriteNote(BaseModel):
    title: str
    description: str

class UpdateNote(BaseModel):
    title: str | None = None
    description: str | None = None