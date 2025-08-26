from fastapi import APIRouter, Depends
from application.interfaces import IDocumentUseCases
from application.dtos import SemanticSearchRequestDTO
from presentation.api.dependencies import get_document_use_cases
from presentation.schemas import SemanticSearchRequest, SemanticSearchResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/semantic", response_model=SemanticSearchResponse)
async def semantic_search(
    request: SemanticSearchRequest,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    dto = SemanticSearchRequestDTO(query=request.query, limit=request.limit)
    result = await use_cases.semantic_search(dto)
    return SemanticSearchResponse.from_dto(result)