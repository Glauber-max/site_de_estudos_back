from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

urlDatBase = "sqlite:///app/database/base/databaseEstudos.sqlite"
db = create_engine(urlDatBase, connect_args={"check_same_thread": False})

Session = sessionmaker(autoflush=False, autocommit=False, bind=db)
session = Session()

Base = declarative_base()

def get_db():
    engine = Session()
    try:
        yield engine
    finally:
        engine.close()