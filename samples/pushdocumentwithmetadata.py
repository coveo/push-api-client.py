from push_api_clientpy import Source, DocumentBuilder

source = Source("my_api_key", "my_org_id")

myDocument = DocumentBuilder("https://my.document.uri", "My document title").withAuthor()