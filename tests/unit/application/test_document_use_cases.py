import pytest
from unittest.mock import Mock, AsyncMock
from application.use_cases import DocumentUseCases
from application.dtos import CreateDocumentDTO, DocumentResponseDTO
from domain.entities import Document

@pytest.fixture
def mock_repositories():
    doc_repo = Mock()
    cache_repo = Mock()
    vector_repo = Mock()
    embedding_service = Mock()
    
    return doc_repo, cache_repo, vector_repo, embedding_service

@pytest.mark.asyncio
async def test_create_document_success(mock_repositories):
    doc_repo, cache_repo, vector_repo, embedding_service = mock_repositories
    
    # Setup mocks
    created_doc = Document(id=1, title="Test", content="Content")
    doc_repo.create = AsyncMock(return_value=created_doc)
    embedding_service.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])
    vector_repo.store_embedding = AsyncMock(return_value=True)
    cache_repo.set = AsyncMock(return_value=True)
    
    # Test
    use_cases = DocumentUseCases(doc_repo, cache_repo, vector_repo, embedding_service)
    dto = CreateDocumentDTO(title="Test", content="Content")
    
    result = await use_cases.create_document(dto)

     # Assertions
    assert isinstance(result, DocumentResponseDTO)
    assert result.title == "Test"
    assert result.content == "Content"
    doc_repo.create.assert_called_once()
    embedding_service