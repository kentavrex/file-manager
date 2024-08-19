import io
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile, HTTPException

from usecases.document import DocumentsUseCase
from usecases.schemas import CreateDocumentSchema, DocumentSchema, RawDocumentSchema


@pytest.fixture
def mock_db_uow():
    mock = AsyncMock()
    mock.document = AsyncMock()

    mock.__aenter__.return_value = mock
    return mock


@pytest.fixture
def mock_s3_repository():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    return mock


@pytest.fixture
def documents_usecase(mock_db_uow, mock_s3_repository):
    return DocumentsUseCase(mock_db_uow, mock_s3_repository)


@pytest.mark.asyncio
async def test_get_all_documents_s3_paths_empty(documents_usecase, mock_db_uow):
    mock_db_uow.document.get_all.return_value = []

    result = await documents_usecase.get_all_documents_s3_paths()

    assert result == []
    mock_db_uow.document.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_documents_s3_paths_with_documents(documents_usecase, mock_db_uow):
    # Arrange
    class MockDocument:
        def __init__(self, id):
            self.id = id

    mock_documents = [MockDocument(1), MockDocument(2), MockDocument(3)]
    mock_db_uow.document.get_all.return_value = mock_documents

    # Act
    result = await documents_usecase.get_all_documents_s3_paths()

    # Assert
    assert result == ["1", "2", "3"]
    mock_db_uow.document.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_files_paths_empty(documents_usecase, mock_s3_repository):
    mock_s3_repository.get_all_files_paths.return_value = []

    result = await documents_usecase.get_all_files_paths()

    assert result == []
    mock_s3_repository.get_all_files_paths.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_files_paths_with_files(documents_usecase, mock_s3_repository):
    mock_file_paths = ["file1.txt", "file2.txt", "file3.txt"]
    mock_s3_repository.get_all_files_paths.return_value = mock_file_paths

    result = await documents_usecase.get_all_files_paths()

    assert result == mock_file_paths
    mock_s3_repository.get_all_files_paths.assert_called_once()


@pytest.mark.asyncio
async def test_get_document_url(documents_usecase, mock_s3_repository):
    # Arrange
    document_id = 1
    expected_url = "https://example.com/download/1"
    mock_s3_repository.get_file_download_link.return_value = expected_url

    # Act
    result = await documents_usecase._get_document_url(document_id)

    # Assert
    assert result == expected_url
    mock_s3_repository.get_file_download_link.assert_called_once_with(file_db_id=document_id)


@pytest.mark.asyncio
async def test_save_file_on_disk(tmp_path, documents_usecase):
    # Arrange
    file_path = tmp_path / "test.txt"
    file_content = "Test content"
    file = UploadFile(filename="test.txt", file=io.BytesIO(file_content.encode()))

    # Act
    result = await documents_usecase._save_file_on_disk(file_path=str(file_path), file=file)

    # Assert
    assert result is None
    assert file_path.read_text() == file_content


@pytest.mark.asyncio
async def test_upload_file(documents_usecase, mock_db_uow, mock_s3_repository):
    # Arrange
    class MockFile:
        def __init__(self, filename, content):
            self.filename = filename
            self.content = content

        async def read(self, size=-1):
            return self.content

        async def seek(self, offset):
            pass

    files = [MockFile("file1.txt", b"content1"), MockFile("file2.txt", b"content2")]
    mock_db_uow.document.create.side_effect = [
        RawDocumentSchema(id=1, name="file1.txt", extension=".txt", format="text/plain", size=len(files[0].content)),
        RawDocumentSchema(id=2, name="file2.txt", extension=".txt", format="text/plain", size=len(files[1].content))]

    # Act
    await documents_usecase.upload_file(files)

    # Assert
    mock_db_uow.document.create.assert_any_call(
        CreateDocumentSchema(name="file1.txt", extension=".txt", format="text/plain", size=len(files[0].content)))
    mock_db_uow.document.create.assert_any_call(
        CreateDocumentSchema(name="file2.txt", extension=".txt", format="text/plain", size=len(files[1].content)))
    mock_s3_repository.upload_file.assert_any_call(file_id=1, file=files[0])
    mock_s3_repository.upload_file.assert_any_call(file_id=2, file=files[1])
