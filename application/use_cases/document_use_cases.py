import json
from typing import List, Optional
from datetime import datetime

from domain.entities import Document, EmbeddingDocument
from domain.repositories import IDocumentRepository, ICacheRepository, IVectorRepository
from domain.services import IEmbeddingService
from application.interfaces import IDocumentUseCases
from application.dtos import (
    CreateDocumentDTO, UpdateDocumentDTO, DocumentResponseDTO,
    SemanticSearchRequestDTO, SemanticSearchResponseDTO, SearchResultDTO
)

class DocumentUseCases(IDocumentUseCases):
    def __init__(
        self,
        doc_repository: IDocumentRepository,
        cache_repository: ICacheRepository,
        vector_repository: IVectorRepository,
        embedding_service: IEmbeddingService
    ):
        self._doc_repository = doc_repository
        self._cache_repository = cache_repository
        self._vector_repository = vector_repository
        self._embedding_service = embedding_service

    async def create_document(self, dto: CreateDocumentDTO) -> DocumentResponseDTO:
        document = Document(title=dto.title, content=dto.content)
        created_doc = await self._doc_repository.create(document)
        
        await self._store_document_embedding(created_doc)
        await self._cache_document(created_doc)
        
        return self._to_response_dto(created_doc)
    
    async def get_document(self, doc_id: int) -> Optional[DocumentResponseDTO]:
        cached_doc = await self._get_cached_document(doc_id)
        if cached_doc:
            return cached_doc
        
        document = await self._doc_repository.get_by_id(doc_id)
        if not document:
            return None
            
            await self._cache_document(document)
        return self._to_response_dto(document)
    
    async def get_all_documents(self, skip: int = 0, limit: int = 100) -> List[DocumentResponseDTO]:
        documents = await self._doc_repository.get_all(skip, limit)
        return [self._to_response_dto(doc) for doc in documents]
    
    async def update_document(self, doc_id: int, dto: UpdateDocumentDTO) -> Optional[DocumentResponseDTO]:
        existing_doc = await self._doc_repository.get_by_id(doc_id)
        if not existing_doc:
            return None
        
        updated_doc = Document(
            id=existing_doc.id,
            title=dto.title if dto.title is not None else existing_doc.title,
            content=dto.content if dto.content is not None else existing_doc.content,
            created_at=existing_doc.created_at
        )
        
        result = await self._doc_repository.update(doc_id, updated_doc)
        if not result:
            return None
        
        await self._cache_document(result)
        await self._store_document_embedding(result)
        
        return self._to_response_dto(result)
    
    async def delete_document(self, doc_id: int) -> bool:
        deleted = await self._doc_repository.delete(doc_id)
        if deleted:
            cache_key = f"doc:{doc_id}"
            await self._cache_repository.delete(cache_key)
        return deleted
    
    async def semantic_search(self, dto: SemanticSearchRequestDTO) -> SemanticSearchResponseDTO:
        query_embedding = await self._embedding_service.generate_embedding(dto.query)
        if not query_embedding:
            return SemanticSearchResponseDTO(
                results=[],
                total_results=0,
                query=dto.query
            )
        search_results = await self._vector_repository.similarity_search(
            query_embedding, dto.limit
        )
        
        result_dtos = [
            SearchResultDTO(
                id=result.id,
                score=result.score,
                content=result.content,
                metadata=result.metadata
            )
            for result in search_results
        ]
        
        return SemanticSearchResponseDTO(
            results=result_dtos,
            total_results=len(result_dtos),
            query=dto.query
        )
    
    async def _store_document_embedding(self, document: Document) -> None:
        embedding = await self._embedding_service.generate_embedding(document.content)
        if embedding:
            embed_doc = EmbeddingDocument(
                id=str(document.id),
                content=document.content,
                embedding=embedding,
                metadata={"title": document.title, "doc_id": document.id}
            )
            await self._vector_repository.store_embedding(embed_doc)
    
    async def _cache_document(self, document: Document) -> None:
        cache_key = f"doc:{document.id}"
        doc_json = json.dumps({
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "updated_at": document.updated_at.isoformat() if document.updated_at else None
        })
        await self._cache_repository.set(cache_key, doc_json)
    
    async def _get_cached_document(self, doc_id: int) -> Optional[DocumentResponseDTO]:
        cache_key = f"doc:{doc_id}"
        cached_data = await self._cache_repository.get(cache_key)
        
        if not cached_data:
            return None
        
        try:
            doc_data = json.loads(cached_data)
            return DocumentResponseDTO(
                id=doc_data["id"],
                title=doc_data["title"],
                content=doc_data["content"],
                created_at=datetime.fromisoformat(doc_data["created_at"]) if doc_data.get("created_at") else None,
                updated_at=datetime.fromisoformat(doc_data["updated_at"]) if doc_data.get("updated_at") else None
            )
        except (json.JSONDecodeError, ValueError):
            return None
    
    def _to_response_dto(self, document: Document) -> DocumentResponseDTO:
        return DocumentResponseDTO(
            id=document.id,
            title=document.title,
            content=document.content,
            created_at=document.created_at,
            updated_at=document.updated_at
        )