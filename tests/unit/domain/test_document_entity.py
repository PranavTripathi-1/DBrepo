import pytest
from datetime import datetime
from domain.entities import Document

def test_document_creation_with_valid_data():
    doc = Document(
        id=1,
        title="Test Title",
        content="Test Content",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert doc.id == 1
    assert doc.title == "Test Title"
    assert doc.content == "Test Content"

def test_document_creation_with_empty_title_raises_error():
    with pytest.raises(ValueError, match="Title and content are required"):
        Document(title="", content="Test Content")

def test_document_creation_with_empty_content_raises_error():
    with pytest.raises(ValueError, match="Title and content are required"):
        Document(title="Test Title", content="")