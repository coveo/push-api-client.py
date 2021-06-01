from dataclasses import dataclass, field
from typing import Literal, Optional, Union

MetadataValue = Union[str, list[str], int, list[int], float, list[float]]
CompressionType = Literal["UNCOMPRESSED", "DEFLATE", "GZIP", "LZMA", "ZLIB"]
SecurityIdentityType = Literal["USER", "GROUP", "VIRTUAL_GROUP", "UNKNOWN"]

@dataclass
class SecurityIdentity:
    identity: str
    identityType: SecurityIdentityType
    securityProvider: str


@dataclass
class Permission:
    allowedPermissions: list[SecurityIdentity] = field(init=False, default_factory=list)
    deniedPermissions: list[SecurityIdentity] = field(init=False, default_factory=list)
    allowAnonymous: bool = field(init=False, default=True)


@dataclass
class CompressedBinaryData:
    compressionType: CompressionType = field(default="UNCOMPRESSED")
    data: str = field(default="")


@dataclass
class Document:
    uri: str
    title: str
    clickableUri: Optional[str] = field(init=False, default="")
    author: Optional[str] = field(init=False, default="")
    date: Optional[str] = field(init=False, default="")
    modifiedDate: Optional[str] = field(init=False, default="")
    permanentId: Optional[str] = field(init=False, default="")
    parentId: Optional[str] = field(init=False, default="")
    data: Optional[str] = field(init=False, default="")
    metadata: Optional[dict[str, MetadataValue]] = field(init=False, default_factory=dict)
    permissions: Optional[list[Permission]] = field(init=False, default_factory=lambda: [Permission()])
    fileExtension: Optional[str] = field(init=False, default="")
    compressedBinaryData: Optional[CompressedBinaryData] = field(init=False, default_factory=lambda: CompressedBinaryData())


