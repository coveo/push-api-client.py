from src.push_api_clientpy import DocumentBuilder
import datetime

docBuilder = DocumentBuilder('id', 'title').withDate(datetime.datetime.now()).withModifiedDateDate(
    "2000/01/01").withClickableUri('https://clicky.uri').withFileExtension('.html').withParentId('parent_id')
print(docBuilder.marshal())
