from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models import Base

# Database connection URL from Railway
DATABASE_URL = "mysql+pymysql://root:efHEJTHSGjmzgHtLPmlgXswGCZpDsiNK@shortline.proxy.rlwy.net:45077/railway"
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
        Base.metadata.create_all(bind=engine) # 📍 Breakpoint 2: This is the critical line.
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}") # 📍 Breakpoint 3: Check if a database connection error occurs here.