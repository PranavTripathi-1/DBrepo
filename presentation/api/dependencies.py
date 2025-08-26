from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import Depends

from infrastructure.database import get_db
from infrastructure.repositories import SQLDocumentRepository, RedisCacheRepository, QdrantVectorRepository
from infrastructure.services import SentenceTransformerService
from application.use_cases import DocumentUseCases
from application.interfaces import IDocumentUseCases

# Singleton instances
@lru_cache()
def get_cache_repository():
    return RedisCacheRepository()

@lru_cache()
def get_vector_repository():
    return QdrantVectorRepository()

@lru_cache()
def get_embedding_service():
    return SentenceTransformerService()

def get_document_use_cases(db: Session = Depends(get_db)) -> IDocumentUseCases:
    doc_repo = SQLDocumentRepository(db)
    cache_repo = get_cache_repository()
    vector_repo = get_vector_repository()
    embedding_service = get_embedding_service()
    
    return DocumentUseCases(doc_repo, cache_repo, vector_repo, embedding_service)
