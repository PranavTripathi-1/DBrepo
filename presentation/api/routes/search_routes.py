from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.database.models import Document

router = APIRouter(prefix="/search")

@router.get("/")
def search_documents(query: str, db: Session = Depends(get_db)):
    """
    Search documents by title or content (case-insensitive).
    """
    results = db.query(Document).filter(
        (Document.title.ilike(f"%{query}%")) |
        (Document.content.ilike(f"%{query}%"))
    ).all()
    return results
