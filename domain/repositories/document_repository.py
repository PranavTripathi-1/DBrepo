from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Document

class IDocumentRepository(ABC):
    @abstractmethod
    async def create(self, document: Document) -> Document:
        pass
    
    @abstractmethod
    async def get_by_id(self, doc_id: int) -> Optional[Document]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        pass
    
    @abstractmethod
    async def update(self, doc_id: int, document: Document) -> Optional[Document]:
        pass
    
    @abstractmethod
    async def delete(self, doc_id: int) -> bool:
        pass