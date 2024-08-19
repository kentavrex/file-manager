from abc import ABC, abstractmethod
from typing import Self

from usecases.interfaces.repositories import DocumentRepositorySQLInterface


class UOWInterface(ABC):
    @abstractmethod
    def __aenter__(self) -> Self: ...

    @abstractmethod
    def __aexit__(self, exc_type, exc_val, exc_tb):  # noqa ANN001
        ...


class DBUnitOfWorkInterface(UOWInterface, ABC):
    document: DocumentRepositorySQLInterface
