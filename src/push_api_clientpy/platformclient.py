from .document import Document, SecurityIdentityType
from dataclasses import asdict, dataclass
from typing import Literal, TypedDict
import requests
import json

SourceVisibility = Literal["PRIVATE", "SECURED", "SHARED"]


@dataclass
class IdentityModel:
    AdditionalInfo: dict[str, str]
    Name: str
    Type: SecurityIdentityType

    def toJSON(self):
        return {
            "additionalInfo": self.AdditionalInfo,
            "name": self.Name,
            "type": self.Type
        }


@dataclass
class AliasMapping(IdentityModel):
    Provider: str

    def toJSON(self):
        return super().toJSON() | {
            "provider": self.Provider
        }


@dataclass
class SecurityIdentityModelBase:
    Identity: IdentityModel
    WellKnowns: list[IdentityModel]

    def toJSON(self):
        return {
            "identity": self.Identity.toJSON(),
            "wellKnowns": list(map(lambda wellKnown: wellKnown.toJSON(), self.WellKnowns)),
        }


@dataclass
class SecurityIdentityModel(SecurityIdentityModelBase):
    Members: list[IdentityModel]

    def toJSON(self):
        return super().toJSON() | {
            "members": list(map(lambda member: member.toJSON(), self.Members))
        }


@dataclass
class SecurityIdentityAliasModel(SecurityIdentityModelBase):
    Mappings: list[AliasMapping]

    def toJSON(self):
        return super().toJSON() | {
            "mappings": list(map(lambda mapping: mapping.toJSON(), self.Mappings))
        }


@dataclass
class SecurityIdentityDelete:
    Identity: IdentityModel

    def toJSON(self):
        return {
            "identity": self.Identity.toJSON()
        }


@dataclass
class SecurityIdentityDeleteOptions:
    QueueDelay: int
    OrderingID: int


@dataclass
class SecurityIdentityBatchConfig:
    FileID: str
    OrderingID: int


@dataclass
class FileContainer:
    uploadUri: str
    fileId: str
    requiredHeaders: dict[str, str]


@dataclass
class BatchDelete:
    documentId: str
    deleteChildren: bool


@dataclass
class BatchUpdateDocuments:
    addOrUpdate: list[Document]
    delete: list[BatchDelete]


class PlatformClient:
    def __init__(self, apikey: str, organizationid: str):
        self.apikey = apikey
        self.organizationid = organizationid

    def createSource(self, name: str, sourceVisibility: SourceVisibility):
        data = {
            "sourceType":  "PUSH",
            "pushEnabled": True,
            "name": name,
            "sourceVisibility": sourceVisibility
        }
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = self.__baseSourceURL()
        return requests.post(url, json=data, headers=headers)

    def createOrUpdateSecurityIdentity(self, securityProviderId: str, securityIdentityModel: SecurityIdentityModel):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return requests.put(url, json=securityIdentityModel.toJSON(), headers=headers)

    def createOrUpdateSecurityIdentityAlias(self, securityProviderId: str, securityIdentityAlias: SecurityIdentityAliasModel):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/mappings'
        return requests.put(url, json=securityIdentityAlias.toJSON(), headers=headers)

    def deleteSecurityIdentity(self, securityProviderId: str,  securityIdentityToDelete: SecurityIdentityDelete):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return requests.delete(url, json=securityIdentityToDelete.toJSON(), headers=headers)

    def deleteOldSecurityIdentities(self, securityProviderId: str, batchDelete: SecurityIdentityDeleteOptions):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/olderthan'
        queryParams = {"orderingId": batchDelete.OrderingID,
                       "queueDelay": batchDelete.QueueDelay}
        return requests.delete(url, params=queryParams, headers=headers)

    def manageSecurityIdentities(self, securityProviderId: str, batchConfig: SecurityIdentityBatchConfig):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/batch'
        queryParams = {"fileId": batchConfig.FileID,
                       "orderingId": batchConfig.OrderingID}
        return requests.delete(url, params=queryParams, headers=headers)

    def pushDocument(self, sourceId: str, doc):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"documentId": doc["documentId"]}
        return requests.put(url, headers=headers, data=json.dumps(doc), params=queryParams)

    def deleteDocument(self, sourceId: str, documentId: str, deleteChildren: bool):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"deleteChildren": str(
            deleteChildren).lower(), "documentId": documentId}
        return requests.delete(url, headers=headers, params=queryParams)

    def createFileContainer(self):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/files'
        return requests.post(url, headers=headers)

    def uploadContentToFileContainer(self, fileContainer: FileContainer, content: BatchUpdateDocuments):
        headers = fileContainer.requiredHeaders
        url = fileContainer.uploadUri
        return requests.put(url, json=asdict(content), headers=headers)

    def pushFileContainerContent(self, sourceId: str, fileContainer: FileContainer):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents/batch'
        queryParams = {"fileId": fileContainer.fileId}
        return requests.put(url=url, params=queryParams, headers=headers)

    def __basePushURL(self):
        return f'https://api.cloud.coveo.com/push/v1/organizations/{self.organizationid}'

    def __basePlatformURL(self):
        return f'https://platform.cloud.coveo.com/rest/organizations/{self.organizationid}'

    def __baseSourceURL(self):
        return f'{self.__basePlatformURL()}/sources'

    def __baseProviderURL(self, providerId: str):
        return f'{self.__basePushURL()}/providers/{providerId}'

    def __authorizationHeader(self):
        return {"Authorization": f'Bearer {self.apikey}'}

    def __contentTypeApplicationJSONHeader(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}
