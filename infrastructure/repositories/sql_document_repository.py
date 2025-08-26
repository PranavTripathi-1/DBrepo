from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories import IDocumentRepository
from domain.entities import Document
from infrastructure.database.models import DocumentModel

class SQLDocumentRepository(IDocumentRepository):
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def create(self, document: Document) -> Document:
        db_doc = DocumentModel(
            title=document.title,
            content=document.content
        )
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)

        return Document(
            id=db_doc.id,
            title=db_doc.title,
            content=db_doc.content,
            created_at=db_doc.created_at,
            updated_at=db_doc.updated_at
        )
    
    async def get_by_id(self, doc_id: int) -> Optional[Document]:
        db_doc = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not db_doc:
            return None
        
        return Document(
            id=db_doc.id,
            title=db_doc.title,
            content=db_doc.content,
            created_at=db_doc.created_at,
            updated_at=db_doc.updated_at
        )
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        db_docs = self.db.query(DocumentModel).offset(skip).limit(limit).all()
        return [
            Document(
                id=doc.id,
                title=doc.title,
                content=doc.content,
                created_at=doc.created_at,
                updated_at=doc.updated_at
            ) for doc in db_docs
        ]
    
    async def update(self, doc_id: int, document: Document) -> Optional[Document]:
        db_doc = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not db_doc:
            return None
        
        db_doc.title = document.title
        db_doc.content = document.content
        self.db.commit()
        self.db.refresh(db_doc)
        
        return Document(
            id=db_doc.id,
            title=db_doc.title,
            content=db_doc.content,
            created_at=db_doc.created_at,
            updated_at=db_doc.updated_at
        )
    
    async def delete(self, doc_id: int) -> bool:
        db_doc = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not db_doc:
            return False
        
        self.db.delete(db_doc)
        self.db.commit()
        return True