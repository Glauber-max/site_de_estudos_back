from fastapi import FastAPI

from src.models import create_table
from src.routes.user_routes import router as user_routes
app = FastAPI()

app.include_router(user_routes, prefix="/user", tags=["user"])

app.get("/")
def home():
    return {"message": "API rodando"}

if __name__ == "__main__":
    create_table()