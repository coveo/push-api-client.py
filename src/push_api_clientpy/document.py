from build.lib.push_api_clientpy import documentbuilder
from enum import Enum
from typing import Union

class CompressionType(Enum):
    UNCOMPRESSED = 'UNCOMPRESSED'
    DEFLATE = 'DEFLATE'
    GZIP = 'GZIP'
    LZMA = 'LZMA'
    ZLIB = 'ZLIB'


class SecurityIdentityType(Enum):
    UNKNOWN = 'UNKNOWN'
    USER = 'USER'
    GROUP = 'GROUP'
    VIRTUAL_GROUP = 'VIRTUAL_GROUP'


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
    Metadata: dict[str, Union[str, list[str], int, list[int], float, list[float]]]
    Permissions: Permission
    FileExtension: str

    def __init__(self, id: str, title: str): 
        self.Uri = id
        self.Title = title
