from api.schemas import OutputDocumentSchema
from usecases.schemas import DocumentSchema


class Formatter:
    @staticmethod
    def format_document(document: DocumentSchema) -> OutputDocumentSchema:
        return OutputDocumentSchema(id=document.id,
                                    url=document.url,
                                    name=document.name,
                                    extension=document.extension,
                                    format=document.format,
                                    size=document.size)
