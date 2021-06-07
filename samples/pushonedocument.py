from push_api_clientpy import Source, DocumentBuilder

source = Source("my_api_key", "my_org_id")

myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
    .withData("these words will be searchable")

response = source.addOrUpdateDocument("my_source_id", myDocument)

print(f"Document added: {response.json()}")
