from enum import Enum
from typing import Union
from .platformclient import SecurityIdentityType

MetadataValue = Union[str, list[str], int, list[int], float, list[float]]

class CompressionType(Enum):
    UNCOMPRESSED = 'UNCOMPRESSED'
    DEFLATE = 'DEFLATE'
    GZIP = 'GZIP'
    LZMA = 'LZMA'
    ZLIB = 'ZLIB'


class SecurityIdentity:
    Identity: str
    IdentityType: SecurityIdentityType
    SecurityProvider: str

class Permission: 
    AllowAnonymous: bool
    AllowedPermissions: list[SecurityIdentity]
    DeniedPermissions: list[SecurityIdentity]

class CompressedBinaryData:
    CompressionType: CompressionType
    Data: str


class Document:
    Uri: str
    Title: str
    ClickableUri: str
    Author: str
    Date: str
    ModifiedDate: str
    PermanentID: str
    ParentID: str
    Data: str
    CompressedBinaryData: CompressedBinaryData
    Metadata: dict[str, MetadataValue]
    Permissions: Permission
    FileExtension: str

    def __init__(self, id: str, title: str): 
        self.Uri = id
        self.Title = title
