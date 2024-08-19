##########################################################################################################
# File should contain celery tasks (functions that will be called like 'celery.task(task_name).s(args)') #
##########################################################################################################
import asyncio
import logging

from config import S3Config
from dependencies import container
from usecases import DocumentsUseCase

logger = logging.getLogger(__name__)
s3_config = S3Config()


def remove_irrelevant_documents() -> None:
    document_service = container.resolve(DocumentsUseCase)

    loop = asyncio.get_event_loop()

    try:
        files_paths = loop.run_until_complete(document_service.get_all_files_paths())
        documents_paths = loop.run_until_complete(document_service.get_all_documents_s3_paths())
        diff = set(files_paths) - set(documents_paths)
        removed = loop.run_until_complete(document_service.delete_files_by_paths(diff))
        logger.info(f"Removed {removed} documents from "
                    f"{s3_config.AWS_S3_ENDPOINT_URL}/{s3_config.AWS_STORAGE_BUCKET_NAME}")
    except RuntimeError as e:
        logging.error(f"Ошибка выполнения задачи: {e}")
