from abc import ABC, abstractmethod
from typing import Iterable

from fastapi import UploadFile

from usecases.schemas import CreateDocumentSchema, RawDocumentSchema


class DocumentRepositorySQLInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[RawDocumentSchema]: ...

    @abstractmethod
    async def create(self, data: CreateDocumentSchema) -> list[RawDocumentSchema]: ...

    @abstractmethod
    async def delete(self, document_id: int) -> list[RawDocumentSchema]: ...


class ObjectsRepositoryInterface(ABC):

    @abstractmethod
    async def upload_file(self, file_id: int, file: UploadFile) -> None:
        ...

    @abstractmethod
    async def get_all_files_paths(self) -> Iterable[str]: ...

    @abstractmethod
    async def delete_files_by_paths(self, paths: Iterable[str]) -> int: ...

    @abstractmethod
    async def get_file_download_link(self, file_db_id: int) -> str: ...
