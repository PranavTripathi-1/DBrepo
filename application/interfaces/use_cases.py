from abc import ABC, abstractmethod
from typing import List, Optional
from application.dtos import (
    CreateDocumentDTO, UpdateDocumentDTO, DocumentResponseDTO,
    SemanticSearchRequestDTO, SemanticSearchResponseDTO
)

class IDocumentUseCases(ABC):
    @abstractmethod
    async def create_document(self, dto: CreateDocumentDTO) -> DocumentResponseDTO:
        pass
    
    @abstractmethod
    async def get_document(self, doc_id: int) -> Optional[DocumentResponseDTO]:
        pass
    
    @abstractmethod
    async def get_all_documents(self, skip: int = 0, limit: int = 100) -> List[DocumentResponseDTO]:
        pass

    @abstractmethod    
    async def update_document(self, doc_id: int, dto: UpdateDocumentDTO) -> Optional[DocumentResponseDTO]:
        pass
    
    @abstractmethod
    async def delete_document(self, doc_id: int) -> bool:
        pass
    
    @abstractmethod
    async def semantic_search(self, dto: SemanticSearchRequestDTO) -> SemanticSearchResponseDTO:
        pass