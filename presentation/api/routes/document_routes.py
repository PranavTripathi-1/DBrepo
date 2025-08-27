from pydoc import doc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.database.models import Document
from domain.entities.document import Document

router = APIRouter(prefix="/documents")

@router.post("/")
def create_document(title: str, content: str, db: Session = Depends(get_db)):
    new_doc = Document(title=doc.title, content=doc.content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

