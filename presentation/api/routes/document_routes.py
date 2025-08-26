from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from application.interfaces import IDocumentUseCases
from application.dtos import CreateDocumentDTO, UpdateDocumentDTO, DocumentResponseDTO
from presentation.api.dependencies import get_document_use_cases
from presentation.schemas import CreateDocumentRequest, UpdateDocumentRequest, DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    request: CreateDocumentRequest,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    dto = CreateDocumentDTO(title=request.title, content=request.content)
    result = await use_cases.create_document(dto)
    return DocumentResponse.from_dto(result)

@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: int,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    result = await use_cases.get_document(doc_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return DocumentResponse.from_dto(result)

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    results = await use_cases.get_all_documents(skip, limit)
    return [DocumentResponse.from_dto(result) for result in results]

@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(
    doc_id: int,
    request: UpdateDocumentRequest,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    dto = UpdateDocumentDTO(title=request.title, content=request.content)
    result = await use_cases.update_document(doc_id, dto)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return DocumentResponse.from_dto(result)

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: int,
    use_cases: IDocumentUseCases = Depends(get_document_use_cases)
):
    deleted = await use_cases.delete_document(doc_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
