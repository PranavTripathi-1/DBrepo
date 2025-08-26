from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Document:
    id: Optional[int] = None
    content: str = ""
    title: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.title or not self.content:
            raise ValueError("Title and content are required")

@dataclass
class EmbeddingDocument:
    id: str
    content: str
    embedding: list[float]
    metadata: dict