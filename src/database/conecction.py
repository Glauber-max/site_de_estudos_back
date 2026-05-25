
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

urlDatBase = "sqlite:///src/database/base/databaseEstudos.sqlite"

db = create_engine(urlDatBase, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=db)
session = SessionLocal()

Base = declarative_base()

def get_db():
    engine = SessionLocal()
    try:
        yield engine
    finally:
        engine.close()
