from fastapi import FastAPI
from src.models import create_table
from src.routes.user_routes import router as user_routes
from src.routes.summary_routes import router as summary_routes
from src.routes.notes_routes import router as notes_routes
from dotenv import load_dotenv
load_dotenv()
import os
os.getenv("SECRET_KEY")
app = FastAPI()

app.include_router(user_routes, prefix="/user", tags=["user"])
app.include_router(summary_routes, prefix="/summary", tags=["summary"])
app.include_router(notes_routes, prefix="/notes", tags=["notes"])
@app.get("/")
def home():
    return {"message": "API rodando"}

if __name__ == "__main__":
    create_table()