from push_api_clientpy.document import Document


class DocumentBuilder:
    document: Document
    def __init__(self, documentId: str, documentTitle: str):
        self.document = Document()
        self.document.uri = documentId
        self.document.title = documentTitle