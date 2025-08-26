from typing import List
from sentence_transformers import SentenceTransformer
from domain.services import IEmbeddingService

class SentenceTransformerService(IEmbeddingService):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    async def generate_embedding(self, text: str) -> List[float]:
        try:
            embedding = self.model.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []