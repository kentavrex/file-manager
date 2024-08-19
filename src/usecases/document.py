import glob
import logging
import mimetypes
import os
from typing import Iterable

import aiofiles
from fastapi import File, UploadFile

from config import settings
from usecases.errors import DiskStorageError, S3Error, StorageError
from usecases.interfaces import DBUnitOfWorkInterface
from usecases.interfaces.repositories import ObjectsRepositoryInterface
from usecases.schemas import CreateDocumentSchema, DocumentSchema, RawDocumentSchema


class DocumentsUseCase:
    def __init__(
            self,
            db_uow: DBUnitOfWorkInterface,
            s3_repository: ObjectsRepositoryInterface,
    ) -> None:
        self._db_uow = db_uow
        self._s3_repository = s3_repository

    async def get_all_documents_s3_paths(self) -> list[str]:
        async with self._db_uow as db_uow:
            documents = await db_uow.document.get_all()
            return [str(d.id) for d in documents]

    async def get_all_files_paths(self) -> Iterable[str]:
        async with self._s3_repository as s3:
            return await s3.get_all_files_paths()

    async def _get_document_url(self, document_id: int) -> str:
        async with self._s3_repository as s3:
            return await s3.get_file_download_link(file_db_id=document_id)

    async def _parse_document(self, document: RawDocumentSchema) -> DocumentSchema:
        logging.info(await self._get_document_url(document.id))
        return DocumentSchema(
            id=document.id,
            name=document.name,
            extension=document.extension,
            format=document.format,
            size=document.size,
            url=await self._get_document_url(document.id),
        )

    async def get_by_id(self, document_id: int) -> DocumentSchema:
        async with self._db_uow as db_uow:
            document = await db_uow.document.get_by_id(document_id)
            return await self._parse_document(document)

    @staticmethod
    async def _save_file_on_disk(file_path: str, file: UploadFile = File(...)) -> None:
        try:
            async with aiofiles.open(file_path, 'wb') as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)
        except Exception as e:
            logging.error(f"Upload file error: {e}")

    @staticmethod
    async def _delete_files_on_disk(file_names: Iterable[str]) -> None:
        try:
            for file_name in file_names:
                pattern = os.path.join(settings.FILES_SAVE_ON_DISK_PATH, f"{file_name}.*")
                files = glob.glob(pattern)
                if not files:
                    logging.warning(f"File {file_name} not found.")
                    continue
                file_path = files[0]
                os.remove(file_path)
                logging.info(f"File removed {file_path}")
        except Exception as e:
            logging.error(f"Delete file error: {e}")

    async def upload_file(self, files: list[UploadFile]) -> None:
        async with (
            self._s3_repository as s3,
            self._db_uow as db_uow,
        ):
            for file in files:
                extension = os.path.splitext(file.filename)[1]
                file_size = len(await file.read())
                await self._rewind_read(file=file)

                try:
                    file_meta_data = await db_uow.document.create(
                        CreateDocumentSchema(name=file.filename,
                                             extension=extension,
                                             format=mimetypes.guess_type(file.filename)[0],
                                             size=file_size),
                    )
                except Exception as error:
                    logging.error(f"DB save {error=}")
                    raise StorageError from error
                file_path = f"{settings.FILES_SAVE_ON_DISK_PATH}{file_meta_data.id}{extension}"

                try:
                    await self._save_file_on_disk(file_path=file_path, file=file)
                except Exception as error:
                    logging.error(f"On dick save {error=}")
                    raise DiskStorageError from error
                else:
                    await self._rewind_read(file=file)

                try:
                    await s3.upload_file(file_id=file_meta_data.id, file=file)
                except Exception as error:
                    logging.error(f"S3 save {error=}")
                    raise S3Error from error

    @staticmethod
    async def _rewind_read(file: UploadFile) -> None:
        """Перемотка файла на начало для последующих операций"""
        await file.seek(0)

    async def delete_files_by_paths(self, paths: Iterable[str]) -> int:
        async with self._s3_repository as s3:
            self._delete_files_on_disk(paths)
            return await s3.delete_files_by_paths(paths)
