"""Here will be stored variables which are related with app"""

from pydantic_settings import BaseSettings


class DatabaseUrlConfig(BaseSettings):
    PG_PORT: str = "5432"
    PG_HOST: str = "app_db"
    PG_DB: str = "test_db"
    PG_USER: str = "test_user"
    PG_PASS: str = "test_password"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


class Settings(BaseSettings):
    APP_REDIS_PREFIX: str = "file-manager:dev"
    CELERY_BROKER_URL: str = "redis://redis:6379"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379"

    DATABASE_URL: str = DatabaseUrlConfig().database_url
    FILES_SAVE_ON_DISK_PATH: str = "/app/data/"


class S3Config(BaseSettings):
    AWS_S3_ENDPOINT_URL: str = "http://minio:9000"
    AWS_S3_ENDPOINT_URL_GET: str = "http://localhost:9000"  # for local run conflicts resolve
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_S3_REGION_NAME: str = "ru-1"
    AWS_STORAGE_BUCKET_NAME: str = "documents"


settings = Settings()
