from app.database.conecction import Base, db
from app.models.agenda import Agenda
from app.models.summary import Summary
from app.models.question import Question
from app.models.user import User
from app.models.notes import Notes

def create_table():
    print("create table")
    Base.metadata.create_all(db)
    print("table created successfully")

if __name__ == "__main__":
    create_table()