#imports for database, i import here because avoid the "circular error".
from src.models.agenda import Agenda
from src.models.summary import Summary
from src.models.question import Question
from src.models.user import User
from src.models.notes import Notes
from src.database.conecction import db, Base

#function created for make a database
def create_table():
    print("create table")
    Base.metadata.create_all(db)
    print("table created successfully")