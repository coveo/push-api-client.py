import base64
from dataclasses import asdict
from datetime import datetime
from typing import Union, cast
import hashlib
from dateutil.parser import parse

from .document import CompressionType, Document, MetadataValue, SecurityIdentity
from .securityidentitybuilder import SecurityIdentityBuilder


class Error(Exception):
    pass


class DocumentBuilder:

    def __init__(self, documentId: str, documentTitle: str):
        self.document = Document(documentId, documentTitle)

    def withData(self, data: str):
        self.document.data = data
        return self

    def withCompressedBinaryData(self, data: str, compressionType: CompressionType):
        self.document.compressedBinaryData.compressionType = compressionType
        self.document.compressedBinaryData.data = data
        return self

    def withDate(self, date: Union[str, int, datetime]):
        self.document.date = self.__validateDateAndReturnValidDate(date)
        return self

    def withModifiedDate(self, date: Union[str, int, datetime]):
        self.document.modifiedDate = self.__validateDateAndReturnValidDate(date)
        return self

    def withPermanentId(self, permanentId: str):
        self.document.permanentId = permanentId
        return self

    def withFileExtension(self, extension: str):
        self.__validateFileExtension(extension)
        self.document.fileExtension = extension
        return self

    def withParentId(self, parentId: str):
        self.document.parentId = parentId
        return self

    def withClickableUri(self, clickURI: str):
        self.document.clickableUri = clickURI
        return self

    def withAuthor(self, author: str):
        self.document.author = author
        return self

    def withMetadataValue(self, key: str, value: MetadataValue):
        self.__validateReservedKeynames(key)
        self.document.metadata[key] = value
        return self

    def withMetadata(self, metadata: dict[str,  MetadataValue]):
        for key in metadata:
            self.withMetadataValue(key, metadata[key])
        return self

    def withAllowedPermissions(self, allowed: SecurityIdentityBuilder):
        self.__setPermissions(allowed, self.document.permissions[0].allowedPermissions)
        return self

    def withDeniedPermissions(self, denied: SecurityIdentityBuilder):
        self.__setPermissions(denied, self.document.permissions[0].deniedPermissions)
        return self

    def withAllowAnonymousUsers(self, allowAnonymous: bool):
        self.document.permissions[0].allowAnonymous = allowAnonymous
        return self

    def marshal(self):
        self.__validateDataAndBinaryData()
        if self.document.permanentId == "":
            self.__generatePermanentId()
        return self.__cleanDocument()

    def __cleanDocument(self):
        withoutEmptyValue = {k: v for k, v in asdict(
            self.document).items() if v is not None and v != ""}

        for k, v in self.document.metadata.items():
            withoutEmptyValue[k] = v
        del withoutEmptyValue['metadata']

        withoutEmptyValue['documentId'] = self.document.uri
        del withoutEmptyValue['uri']

        if self.document.compressedBinaryData.data != "":
            withoutEmptyValue['compressedBinaryData'] = self.document.compressedBinaryData.data
            withoutEmptyValue['compressionType'] = self.document.compressedBinaryData.compressionType
        else:
            del withoutEmptyValue['compressedBinaryData']

        return withoutEmptyValue

    def __generatePermanentId(self):
        # generate a 60-character id
        utf8 = self.document.uri.encode('utf-8')
        md5 = hashlib.md5(utf8)
        sha1 = hashlib.sha1(utf8)
        self.document.permanentId = md5.hexdigest()[:30] + sha1.hexdigest()[:30]

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

    def __setPermissions(self, securityIdentityBuilder: SecurityIdentityBuilder, permissionSection: list[SecurityIdentity]):
        identities = securityIdentityBuilder.build()
        if type(identities) is list:
            permissionSection.extend(identities)
        else:
            permissionSection.append(identities)

    def __validateDataAndBinaryData(self):
        if self.document.data != "" and self.document.compressedBinaryData.data != "":
            raise Error(self, 'Cannot set both data and binary data on the same document')
