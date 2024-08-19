from punq import Container
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import S3Config, settings
from repositories.s3_repository.document import DocumentS3Repository
from uow.sql_uow import SQLUOW
from usecases import DocumentsUseCase
from usecases.interfaces import DBUnitOfWorkInterface, ObjectsRepositoryInterface

s3_config = S3Config()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
)

session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

container = Container()

container.register(DBUnitOfWorkInterface, factory=SQLUOW, session_factory=session_factory)

container.register(
    ObjectsRepositoryInterface,
    factory=DocumentS3Repository,
    config=s3_config,
)

container.register(DocumentsUseCase, factory=DocumentsUseCase)
