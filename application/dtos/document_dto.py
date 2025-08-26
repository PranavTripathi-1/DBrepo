from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class CreateDocumentDTO(BaseModel):
    title: str
    content: str
    
    @validator('title', 'content')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class UpdateDocumentDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    @validator('title', 'content', pre=True)
    def validate_not_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty if provided')
        return v.strip() if v else v

class DocumentResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SemanticSearchRequestDTO(BaseModel):
    query: str
    limit: int = 10
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()
    
    @validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Limit must be between 1 and 100')
        return v

class SearchResultDTO(BaseModel):
    id: str
    score: float
    content: str
    metadata: dict

class SemanticSearchResponseDTO(BaseModel):
    results: List[SearchResultDTO]
    total_results: int
    query: str