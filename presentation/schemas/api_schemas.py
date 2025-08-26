from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from application.dtos import DocumentResponseDTO, SemanticSearchResponseDTO

class CreateDocumentRequest(BaseModel):
    title: str
    content: str
    
    @validator('title', 'content')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    class UpdateDocumentRequest(BaseModel):
        title: Optional[str] = None
    content: Optional[str] = None
    
    @validator('title', 'content', pre=True)
    def validate_not_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty if provided')
        return v.strip() if v else v

class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dto(cls, dto: DocumentResponseDTO):
        return cls(
            id=dto.id,
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

class SemanticSearchRequest(BaseModel):
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

class SearchResultResponse(BaseModel):
    id: str
    score: float
    content: str
    metadata: dict

class SemanticSearchResponse(BaseModel):
    results: List[SearchResultResponse]
    total_results: int
    query: str
    
    @classmethod
    def from_dto(cls, dto: SemanticSearchResponseDTO):
        return cls(
            results=[
                SearchResultResponse(
                    id=result.id,
                    score=result.score,
                    content=result.content,
                    metadata=result.metadata
                ) for result in dto.results
            ],
            total_results=dto.total_results,
            query=dto.query
        )
    