from . import Document


class DocumentBuilder:
    document: Document
    def __init__(self, documentId: str, documentTitle: str):
        self.document = Document(documentId, documentTitle)