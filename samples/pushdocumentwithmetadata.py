from push_api_clientpy import Source, DocumentBuilder, BackoffOptions

source = Source("my_api_key", "my_org_id", BackoffOptions(max_retries=3))

myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
    .withAuthor("bob")\
    .withData("these words will be searchable")\
    .withClickableUri('https://my.document.click.com')\
    .withData('these words will be searchable')\
    .withFileExtension('.html')\
    .withMetadata({
        # A field should be created in the organization and mapped to the source for these to be available on documents
        # See https://docs.coveo.com/en/1833
        "tags": ['the_first_tag', 'the_second_tag'],
        "version": 1,
        "somekey": "some value",
    })

source.addOrUpdateDocument("my_source_id", myDocument)
