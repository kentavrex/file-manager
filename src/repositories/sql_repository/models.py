"""DB models. Works under alembic"""

from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    extension: Mapped[str] = mapped_column(String(150), nullable=True)
    format: Mapped[str] = mapped_column(String(150), nullable=True)
    size: Mapped[int] = mapped_column(nullable=False)

