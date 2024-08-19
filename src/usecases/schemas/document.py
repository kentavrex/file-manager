from pydantic import BaseModel


class RawDocumentSchema(BaseModel):
    id: int
    name: str
    extension: str
    format: str
    size: int


class DocumentSchema(BaseModel):
    id: int
    url: str
    name: str
    extension: str
    format: str
    size: int


class CreateDocumentSchema(BaseModel):
    name: str
    extension: str
    format: str
    size: int

