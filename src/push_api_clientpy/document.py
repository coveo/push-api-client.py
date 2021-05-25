from dataclasses import dataclass, field
from typing import Literal, Optional, Union
from .platformclient import SecurityIdentityType

MetadataValue = Union[str, list[str], int, list[int], float, list[float]]
CompressionType = Literal["UNCOMPRESSED", "DEFLATE", "GZIP", "LZMA", "ZLIB"]


@dataclass
class SecurityIdentity:
    Identity: str
    IdentityType: SecurityIdentityType
    SecurityProvider: str


@dataclass
class Permission:
    AllowedPermissions: list[SecurityIdentity] = field(init=False)
    DeniedPermissions: list[SecurityIdentity] = field(init=False)
    AllowAnonymous: bool = field(init=False, default=True)


@dataclass
class CompressedBinaryData:
    CompressionType: CompressionType
    Data: str

@dataclass
class Document:
    Uri: str
    Title: str
    ClickableUri: Optional[str] = field(init=False)
    Author: Optional[str] = field(init=False)
    Date: Optional[str] = field(init=False)
    ModifiedDate: Optional[str] = field(init=False)
    PermanentID: Optional[str] = field(init=False)
    ParentID: Optional[str] = field(init=False)
    Data: Optional[str] = field(init=False)
    Metadata: Optional[dict[str, MetadataValue]] = field(init=False)
    Permissions: Optional[Permission] = field(init=False)
    FileExtension: Optional[str] = field(init=False)