import logging

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import DataError, DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from usecases.errors import NotFoundError, StorageConstraintError, StorageFKError

logger = logging.getLogger(__name__)


def handle_db_errors(f):  # noqa
    """Декоратор для отлова ошибок базы и инициирования ошибок хранилища"""

    def inner(*args, **kwargs):  # noqa
        try:
            return f(*args, **kwargs)
        except IntegrityError as e:
            logger.error(e.detail)
            raise StorageFKError(e.orig) from e
        except DataError as e:
            logger.error(e.detail)
            raise StorageConstraintError(e.orig) from e
        except DatabaseError as e:
            logger.error(e.detail)
            raise StorageConstraintError(e.orig) from e

    return inner


class BaseSQLRepository:
    model = None
    schema = None

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_all(self, limit: int = 100, skip: int = 0) -> list[schema]:
        query = select(self.model).offset(skip).limit(limit)
        objects = (await self._db.scalars(query)).all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in objects]

    async def get_by_id(self, object_id: int) -> schema:
        query = select(self.model).where(self.model.id == object_id)
        obj = (await self._db.scalars(query)).first()
        if obj is None:
            raise NotFoundError(f"'{self.model.__name__}' id={object_id} object not found")
        return self.schema.model_validate(obj, from_attributes=True)

    @handle_db_errors
    async def create(self, data: BaseModel) -> schema:
        element_created = self.model(**data.model_dump())
        self._db.add(element_created)
        await self._db.commit()
        await self._db.refresh(element_created)
        return self.schema.model_validate(element_created, from_attributes=True)

    @handle_db_errors
    async def update(self, object_id: int, data: BaseModel) -> schema:
        select_query = select(self.model).where(self.model.id == object_id)
        obj = (await self._db.scalars(select_query)).first()
        if obj is None:
            raise NotFoundError(f"'{self.model.__name__}' id={object_id} object not found")
        update_data = data.model_dump(exclude_unset=True)
        update_query = update(self.model).where(self.model.id == object_id).values(**update_data)
        await self._db.execute(update_query)
        await self._db.commit()
        await self._db.refresh(obj)
        return self.schema.model_validate(obj, from_attributes=True)

    @handle_db_errors
    async def delete(self, object_id: int) -> None:
        query = delete(self.model).where(self.model.id == object_id)
        await self._db.execute(query)
        await self._db.commit()
