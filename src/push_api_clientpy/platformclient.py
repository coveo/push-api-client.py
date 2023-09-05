from .document import Document, SecurityIdentityType
from dataclasses import asdict, dataclass
from typing import Literal, TypedDict
import time
import requests
import json

SourceVisibility = Literal["PRIVATE", "SECURED", "SHARED"]
DEFAULT_RETRY_AFTER = 5
DEFAULT_MAX_RETRIES = 50
DEFAULT_TIME_MULTIPLE = 2


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
    def __init__(self, apikey: str, organizationid: str, retry_after = DEFAULT_RETRY_AFTER, max_retries = DEFAULT_MAX_RETRIES, time_mutiple = DEFAULT_TIME_MULTIPLE):
        self.apikey = apikey
        self.organizationid = organizationid
        self.retry_after = retry_after
        self.max_retries = max_retries
        self.time_multiple = time_mutiple

    def createSource(self, name: str, sourceVisibility: SourceVisibility):
        data = {
            "sourceType":  "PUSH",
            "pushEnabled": True,
            "name": name,
            "sourceVisibility": sourceVisibility
        }
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = self.__baseSourceURL()
        return self.call_api_with_retries('post', url, data=data)

    def createOrUpdateSecurityIdentity(self, securityProviderId: str, securityIdentityModel: SecurityIdentityModel):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return self.call_api_with_retries('put',url, json=securityIdentityModel.toJSON(), headers=headers)

    def createOrUpdateSecurityIdentityAlias(self, securityProviderId: str, securityIdentityAlias: SecurityIdentityAliasModel):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/mappings'
        return self.call_api_with_retries('put',url, json=securityIdentityAlias.toJSON(), headers=headers)

    def deleteSecurityIdentity(self, securityProviderId: str,  securityIdentityToDelete: SecurityIdentityDelete):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return self.call_api_with_retries('delete', url, json=securityIdentityToDelete.toJSON(), headers=headers)

    def deleteOldSecurityIdentities(self, securityProviderId: str, batchDelete: SecurityIdentityDeleteOptions):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/olderthan'
        queryParams = {"orderingId": batchDelete.OrderingID,
                       "queueDelay": batchDelete.QueueDelay}
        return self.call_api_with_retries('delete', url, params=queryParams, headers=headers)

    def manageSecurityIdentities(self, securityProviderId: str, batchConfig: SecurityIdentityBatchConfig):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/batch'
        queryParams = {"fileId": batchConfig.FileID,
                       "orderingId": batchConfig.OrderingID}
        return self.call_api_with_retries('put', url, params=queryParams, headers=headers)

    def pushDocument(self, sourceId: str, doc):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"documentId": doc["documentId"]}
        return self.call_api_with_retries('put',url, headers=headers, data=json.dumps(doc), params=queryParams)

    def deleteDocument(self, sourceId: str, documentId: str, deleteChildren: bool):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"deleteChildren": str(
            deleteChildren).lower(), "documentId": documentId}
        return self.call_api_with_retries('delete',url, headers=headers, params=queryParams)

    def createFileContainer(self):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/files'
        return self.call_api_with_retries('post', url, headers=headers)

    def uploadContentToFileContainer(self, fileContainer: FileContainer, content: BatchUpdateDocuments):
        headers = fileContainer.requiredHeaders
        url = fileContainer.uploadUri
        return self.call_api_with_retries('put',url, json=asdict(content), headers=headers)

    def pushFileContainerContent(self, sourceId: str, fileContainer: FileContainer):
        headers = self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader()
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents/batch'
        queryParams = {"fileId": fileContainer.fileId}
        return self.call_api_with_retries('put',url=url, params=queryParams, headers=headers)

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

    def call_api_with_retries(self,
                              method: str,
                              call_endpoint: str,
                              data: _Data | None = ...,
                              headers: _HeadersMapping | None = ...,
                              params: _Params | None = ...,
                              json: Incomplete | None = ...
                            ):
        nb_retries = 0
        delay_in_seconds = self.retry_after
        while True:
            response = requests.request(method, call_endpoint, data=data, headers=headers, params=params, json=json)
            if response.status_code == 429 and nb_retries < self.max_retries:
                time.sleep(delay_in_seconds)
                delay_in_seconds = delay_in_seconds * self.time_multiple
                nb_retries += 1
            else:
                response.raise_for_status()
                return response
