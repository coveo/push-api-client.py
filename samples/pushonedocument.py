from push_api_clientpy import Source, DocumentBuilder, BackoffOptions

source = Source("my_api_key", "my_org_id", backoff_options=BackoffOptions(3, 5))

myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
    .withData("these words will be searchable")

response = source.addOrUpdateDocument("my_source_id", myDocument)

print(f"Document added: {response.json()}")
