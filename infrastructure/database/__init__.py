from .connection import engine, SessionLocal, get_db
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
