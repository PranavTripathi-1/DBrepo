from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# SQLAlchemy engine
engine = create_engine(settings.database_url, echo=True, future=True)

# Session local class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
