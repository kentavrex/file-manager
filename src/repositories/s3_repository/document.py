import logging
from typing import Iterable

import aioboto3
from fastapi import UploadFile

from config import S3Config
from repositories.s3_repository import handle_s3_errors
from usecases.interfaces.repositories import ObjectsRepositoryInterface

logger = logging.getLogger(__name__)


class DocumentS3Repository(ObjectsRepositoryInterface):

    async def __aenter__(self) -> "DocumentS3Repository":
        session = aioboto3.Session()

        self._resource = await session.resource(
            service_name="s3",
            endpoint_url=self._config.AWS_S3_ENDPOINT_URL,
            region_name=self._config.AWS_S3_REGION_NAME,
            aws_access_key_id=self._config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self._config.AWS_SECRET_ACCESS_KEY,
        ).__aenter__()

        self._client = await session.client(
            service_name="s3",
            endpoint_url=self._config.AWS_S3_ENDPOINT_URL_GET,
            region_name=self._config.AWS_S3_REGION_NAME,
            aws_access_key_id=self._config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self._config.AWS_SECRET_ACCESS_KEY,
        ).__aenter__()
        self._bucket = await self._resource.Bucket(self._config.AWS_STORAGE_BUCKET_NAME)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        await self._resource.__aexit__(exc_type, exc_val, exc_tb)
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    def __init__(self, config: S3Config) -> None:
        self._bucket_name = config.AWS_STORAGE_BUCKET_NAME
        self._config = config

    @handle_s3_errors
    async def upload_file(self, file_id: int, file: UploadFile) -> None:
        await self._bucket.put_object(Key=str(file_id), Body=file.file)

    async def _get_all(self):  # noqa
        return self._bucket.objects.all()

    async def _get_presigned_url(self, file_key: str) -> str:
        return await self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket_name, "Key": file_key},
        )

    @handle_s3_errors
    async def get_file_download_link(self, file_db_id: int) -> Iterable[str]:
        return await self._get_presigned_url(str(file_db_id))

    @handle_s3_errors
    async def get_all_files_paths(self) -> list[str]:
        return [f"{file.key}" async for file in await self._get_all()]

    @handle_s3_errors
    async def delete_files_by_paths(self, paths: Iterable[str]) -> int:
        """Returns number of removed rows"""
        removed_files = 0
        files = await self._get_all()

        async for file in files:
            if file.key in paths:
                await file.delete()
                removed_files += 1
        return removed_files
