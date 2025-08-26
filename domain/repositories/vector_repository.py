from abc import ABC, abstractmethod
from typing import List
from domain.entities import EmbeddingDocument
from domain.value_objects import SearchResult

class IVectorRepository(ABC):
    @abstractmethod
    async def store_embedding(self, doc: EmbeddingDocument) -> bool:
        pass
    
    @abstractmethod
    async def similarity_search(self, query_embedding: List[float], limit: int = 10) -> List[SearchResult]:
        pass