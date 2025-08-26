from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from domain.repositories import IVectorRepository
from domain.entities import EmbeddingDocument
from domain.value_objects import SearchResult
from config.settings import settings

class QdrantVectorRepository(IVectorRepository):
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        self.collection_name = "documents"
        self._ensure_collection()
    
    def _ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            if not any(col.name == self.collection_name for col in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
        except Exception as e:
            print(f"Error ensuring collection: {e}")
    
    async def store_embedding(self, doc: EmbeddingDocument) -> bool:
        try:
            point = PointStruct(
                id=doc.id,
                vector=doc.embedding,
                payload={
                    "content": doc.content,
                    **doc.metadata
                }
            )
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            return True
        except Exception as e:
            print(f"Error storing embedding: {e}")
            return False
    
    async def similarity_search(self, query_embedding: List[float], limit: int = 10) -> List[SearchResult]:
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )
            
            return [
                SearchResult(
                    id=str(result.id),
                    score=float(result.score),
                    content=result.payload.get("content", ""),
                    metadata={k: v for k, v in result.payload.items() if k != "content"}
                )
                for result in results
            ]
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
            embedding=document.embedding,
            content=document.content,
            metadata={"title": document.title}
          