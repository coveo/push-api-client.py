import base64
from dataclasses import asdict
import json
from datetime import datetime
from typing import Union, cast
from dateutil.parser import parse
from .document import CompressedBinaryData, CompressionType, Document, MetadataValue, Permission


class Error(Exception):
    pass

class DocumentBuilder:

    def __init__(self, documentId: str, documentTitle: str):
        self.document = Document(Uri=documentId, Title=documentTitle)

    def withData(self, data: str):
        self.document.Data = data
        return self

    def withDate(self, date: Union[str, int, datetime]):
        self.document.Date = self.__validateDateAndReturnValidDate(date)
        return self

    def withModifiedDate(self, date: Union[str, int, datetime]):
        self.document.ModifiedDate = self.__validateDateAndReturnValidDate(date)
        return self

    def withPermanentId(self, permanentId: str):
        self.document.PermanentID = permanentId
        return self

    def withFileExtension(self, extension: str):
        self.__validateFileExtension(extension)
        self.document.FileExtension = extension
        return self

    def withParentId(self, parentId: str):
        self.document.ParentID = parentId
        return self

    def withClickableUri(self, clickURI: str):
        self.document.ClickableUri = clickURI
        return self

    def withMetadataValue(self, key: str, value: MetadataValue):
        self.__validateReservedKeynames(key)
        if self.document.Metadata is None:
            self.document.Metadata = dict()
        self.document.Metadata[key] = value
        return self

    def withMetadata(self, metadata: dict[str,  MetadataValue]):
        for key in metadata:
            self.withMetadataValue(key, metadata[key])
        return self

    def withAllowedPermissions(self):
        # TODO
        return self

    def withDeniedPermissions(self):
        # TODO
        return self

    def withAllowAnonymousUsers(self, allowAnonymous: bool):
        if self.document.Permissions is None:
            self.document.Permissions = Permission()
        self.document.Permissions.AllowAnonymous = allowAnonymous
        return self

    def marshal(self):
        # TODO global validation + fill missing
        # TODO marshal binary data
        # TODO marshal permissions

        return asdict(self.document)

    def __validateDateAndReturnValidDate(self, date: Union[str, int, datetime]) -> str:
        dateAsDatetime = datetime.now()

        if type(date) is str:
            dateAsDatetime = parse(str(date))
            datetime.fromordinal
        if type(date) is int:
            dateAsDatetime = datetime.fromtimestamp(cast(int, date))
        if type(date) is datetime:
            dateAsDatetime = cast(datetime, date)

        if type(dateAsDatetime) is not datetime:
            raise Error(self, "Unable to convert date to valid datetime", date)

        return dateAsDatetime.isoformat()

    def __validateCompressedBinaryData(self, data: str):
        isBase64 = base64.b64encode(base64.b64decode(data)) == data
        if not isBase64:
            raise Error(
                self, "Invalid compressedBinaryData: When using compressedBinaryData, the data must be base64 encoded.")

    def __validateFileExtension(self, ext: str):
        if ext[0] != ".":
            raise Error(self, f'Extension {ext} should start with a leading .')

    def __validateReservedKeynames(self, keyName: str):
        reservedNames = ["compressedBinaryData",
                         "compressedBinaryDataFileId",
                         "parentId",
                         "fileExtension",
                         "data",
                         "permissions",
                         "documentId",
                         "orderingId"]
        for reserved in reservedNames:
            if keyName == reserved:
                raise Error(
                    self, f'Cannot use ${keyName} as a metadata key: It is a reserved key name. See https://docs.coveo.com/en/78/index-content/push-api-reference#json-document-reserved-key-names')
