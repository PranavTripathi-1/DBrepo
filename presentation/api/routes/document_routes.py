from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.database.models import Document as DocumentModel  # SQLAlchemy model
from domain.entities.document import Document as DocumentEntity     # Domain entity
from infrastructure.database.models import Document 
router = APIRouter()

@router.post("/documents")
def create_document(title: str, content: str, db: Session = Depends(get_db)):
    # Create SQLAlchemy model instance
    new_doc = DocumentModel(title=title, content=content)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

