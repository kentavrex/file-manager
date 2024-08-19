import logging
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sql_repository.document import DocumentRepositorySQL
from usecases.interfaces import DBUnitOfWorkInterface


class SQLUOW(DBUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> DBUnitOfWorkInterface:
        self._session = self._session_factory()
        logging.debug(f"Initialized SQL DB connection id={id(self._session)}")
        self.document = DocumentRepositorySQL(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa
        logging.debug(f"Closing SQL DB connection id={id(self._session)}")
        await self._close()

    async def _close(self) -> None:
        await self._session.close()
