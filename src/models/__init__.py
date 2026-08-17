#imports for database, i import here because avoid the "circular error".
from src.models.agenda import Agenda
from src.models.summary import Summary
from src.models.question import Question
from src.models.user import User
from src.models.notes import Notes
from src.models.token_user import TokenValidation
from src.database.conecction import db, Base
import os
#function created for make a database
def create_table():
    os.makedirs('src/database/base', exist_ok=True)
    print("create table")
    Base.metadata.create_all(db)
    print("table created successfully")