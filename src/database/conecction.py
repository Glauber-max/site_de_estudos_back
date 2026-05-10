from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#needs imports

#url used
urlDatBase = "sqlite:///src/database/base/databaseEstudos.sqlite"
#database engine created with multtreads
db = create_engine(urlDatBase, connect_args={"check_same_thread": False})

#open session for use the database (easy acess)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db)
session = SessionLocal()

#variable used for transform command sql in inherited class
Base = declarative_base()

#function used for better performance (open a session and return this, if case happen as error, it close a session)
def get_db():
    engine = SessionLocal()
    try:
        yield engine
    finally:
        engine.close()