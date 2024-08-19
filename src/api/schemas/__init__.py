from typing import Generic, TypeVar

from pydantic import BaseModel

from .document import OutputDocumentSchema

T = TypeVar("T")


class GenericListOutputSchema(BaseModel, Generic[T]):
    data: list[T]
