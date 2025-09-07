from dotenv import load_dotenv
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models import Base

load_dotenv()  # Load environment variables from .env file

# Database connection URL from Railway
DATABASE_URL = os.getenv("DATABASE_URL")
# You should replace this with your actual Railway database connection string.

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL) # 📍 Breakpoint 1: Check if the engine is created successfully.

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """
    Creates all tables defined in SQLAlchemy models if they don't already exist.
    """
    try:
        print("Attempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Handle the error (e.g., log it, raise an exception, etc.)
        raise
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()