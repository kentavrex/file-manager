from pydantic import BaseModel


class OutputDocumentSchema(BaseModel):
    id: int | None = None
    url: str
    name: str
    extension: str
    format: str
    size: int


