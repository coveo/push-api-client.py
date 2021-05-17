from src.push_api_clientpy import DocumentBuilder
import datetime

docBuilder = DocumentBuilder('id', 'title')\
    .withDate(datetime.datetime.now())\
    .withModifiedDate("2000/01/01")\
    .withClickableUri('https://clicky.uri')\
    .withFileExtension('.html')\
    .withParentId('parent_id')\
    .withMetadata({"foo": "bar", "bar": ["buzz"]})\
    .withMetadataValue("hello", [1, 2, 3])


print(docBuilder.marshal())
