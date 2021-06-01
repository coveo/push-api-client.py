from push_api_clientpy import DocumentBuilder


class TestDocBuilder:
    def testMarshalDocumentId(self):
        docBuilder = DocumentBuilder("https://foo.com", "title")
        assert docBuilder.marshal().get('documentId') == "https://foo.com"
