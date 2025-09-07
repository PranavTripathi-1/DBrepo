from .connection import engine, SessionLocal, get_db
from .models import Base

__all__ = ["engine", "SessionLocal", "get_db", "Base"]
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")