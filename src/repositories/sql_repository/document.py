import logging

from repositories.sql_repository import BaseSQLRepository
from repositories.sql_repository.models import Document
from usecases.interfaces.repositories import DocumentRepositorySQLInterface
from usecases.schemas import RawDocumentSchema

logger = logging.getLogger(__name__)


class DocumentRepositorySQL(BaseSQLRepository, DocumentRepositorySQLInterface):
    model = Document
    schema = RawDocumentSchema
