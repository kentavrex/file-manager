from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    def __enter__(self):  # noqa
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # noqa
        self._close()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError
