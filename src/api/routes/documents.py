from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette import status

from api.formatter import Formatter
from api.schemas import OutputDocumentSchema
from dependencies import container
from usecases import DocumentsUseCase
from usecases.errors import DiskStorageError, S3Error, StorageError

router = APIRouter()


@router.get("/{document_id}", response_model=OutputDocumentSchema)
async def get_document_by_id(document_id: int) -> OutputDocumentSchema:
    documents_uc: DocumentsUseCase = container.resolve(DocumentsUseCase)
    document = await documents_uc.get_by_id(document_id=document_id)
    return Formatter.format_document(document)


@router.post("")
async def upload_document_file(
        files: list[UploadFile] = File(description="Multiple files as 'UploadFile' objects"),
) -> None:
    documents_uc: DocumentsUseCase = container.resolve(DocumentsUseCase)
    try:
        await documents_uc.upload_file(files=files)
    except (StorageError, DiskStorageError, S3Error) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {e}",
        ) from e
