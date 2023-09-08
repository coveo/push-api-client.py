from push_api_clientpy import Source, DocumentBuilder, BatchUpdate, BackoffOptions
from push_api_clientpy.platformclient import BatchDelete

source = Source("my_api_key", "my_org_id", BackoffOptions(3, 10, 3))


myBatchOfDocuments = BatchUpdate(addOrUpdate=[], delete=[])

firstDocumentToAdd = DocumentBuilder(
    "https://my.document.uri?ref=1", "My first document title"),

secondDocumentToAdd = DocumentBuilder(
    "https://my.document.uri?ref=2", "My second document title")

firstDocumentToDelete = BatchDelete("https://my.document.uri?ref=3", True)

myBatchOfDocuments.addOrUpdate.append(firstDocumentToAdd)
myBatchOfDocuments.addOrUpdate.append(secondDocumentToAdd)
myBatchOfDocuments.delete.append(firstDocumentToDelete)


response = source.batchUpdateDocuments("my_source_id", myBatchOfDocuments)

print(f"Batch processed: {response.json()}")
