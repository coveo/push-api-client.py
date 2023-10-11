from .document import Document, SecurityIdentityType
from dataclasses import asdict, dataclass
from typing import Literal
import requests
from requests.adapters import HTTPAdapter, Retry
import json
import importlib.metadata

SourceVisibility = Literal["PRIVATE", "SECURED", "SHARED"]
DEFAULT_RETRY_AFTER = 5
DEFAULT_MAX_RETRIES = 50


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

@dataclass
class BackoffOptions:
    retry_after: int = DEFAULT_RETRY_AFTER
    max_retries: int = DEFAULT_MAX_RETRIES


class PlatformClient:
    def __init__(self, apikey: str, organizationid: str, backoff_options: BackoffOptions = BackoffOptions(), session = requests.Session()):
        self.apikey = apikey
        self.organizationid = organizationid
        self.backoff_options = backoff_options

        self.retries = Retry(total=self.backoff_options.max_retries,
                        backoff_factor=self.backoff_options.retry_after,
                        status_forcelist=[429],
                        respect_retry_after_header=False
                        )
        session.mount('https://', HTTPAdapter(max_retries=self.retries))
        self.session = session
        self.version = importlib.metadata.version('coveo-push-api-client.py')

    def createSource(self, name: str, sourceVisibility: SourceVisibility):
        data = {
            "sourceType":  "PUSH",
            "pushEnabled": True,
            "name": name,
            "sourceVisibility": sourceVisibility
        }
        url = self.__baseSourceURL()
        return self.session.post(url, json=data, headers=self.__headers())

    def createOrUpdateSecurityIdentity(self, securityProviderId: str, securityIdentityModel: SecurityIdentityModel):
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return self.session.put(url, json=securityIdentityModel.toJSON(), headers=self.__headers())

    def createOrUpdateSecurityIdentityAlias(self, securityProviderId: str, securityIdentityAlias: SecurityIdentityAliasModel):
        url = f'{self.__baseProviderURL(securityProviderId)}/mappings'
        return self.session.put(url, json=securityIdentityAlias.toJSON(), headers=self.__headers())

    def deleteSecurityIdentity(self, securityProviderId: str,  securityIdentityToDelete: SecurityIdentityDelete):
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions'
        return self.session.delete(url, json=securityIdentityToDelete.toJSON(), headers=self.__headers())

    def deleteOldSecurityIdentities(self, securityProviderId: str, batchDelete: SecurityIdentityDeleteOptions):
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/olderthan'
        queryParams = {"orderingId": batchDelete.OrderingID,
                       "queueDelay": batchDelete.QueueDelay}
        return self.session.delete(url, params=queryParams, headers=self.__headers())

    def manageSecurityIdentities(self, securityProviderId: str, batchConfig: SecurityIdentityBatchConfig):
        url = f'{self.__baseProviderURL(securityProviderId)}/permissions/batch'
        queryParams = {"fileId": batchConfig.FileID,
                       "orderingId": batchConfig.OrderingID}
        return self.session.put(url, params=queryParams, headers=self.__headers())

    def pushDocument(self, sourceId: str, doc):
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"documentId": doc["documentId"]}
        return self.session.put(url, headers=self.__headers(), data=json.dumps(doc), params=queryParams)

    def deleteDocument(self, sourceId: str, documentId: str, deleteChildren: bool):
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents'
        queryParams = {"deleteChildren": str(
            deleteChildren).lower(), "documentId": documentId}
        return self.session.delete(url, headers=self.__headers(), params=queryParams)

    def createFileContainer(self):
        url = f'{self.__basePushURL()}/files'
        return self.session.post(url, headers=self.__headers())

    def uploadContentToFileContainer(self, fileContainer: FileContainer, content: BatchUpdateDocuments):
        url = fileContainer.uploadUri
        return self.session.put(url, json=asdict(content), headers=fileContainer.requiredHeaders)

    def pushFileContainerContent(self, sourceId: str, fileContainer: FileContainer):
        url = f'{self.__basePushURL()}/sources/{sourceId}/documents/batch'
        queryParams = {"fileId": fileContainer.fileId}
        return self.session.put(url=url, params=queryParams, headers=self.__headers())

    def __basePushURL(self):
        return f'https://api.cloud.coveo.com/push/v1/organizations/{self.organizationid}'

    def __basePlatformURL(self):
        return f'https://platform.cloud.coveo.com/rest/organizations/{self.organizationid}'

    def __baseSourceURL(self):
        return f'{self.__basePlatformURL()}/sources'

    def __baseProviderURL(self, providerId: str):
        return f'{self.__basePushURL()}/providers/{providerId}'

    def __headers(self):
        return self.__authorizationHeader() | self.__contentTypeApplicationJSONHeader() | self.__userAgentHeader()

    def __authorizationHeader(self):
        return {"Authorization": f'Bearer {self.apikey}'}

    def __contentTypeApplicationJSONHeader(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __userAgentHeader(self):
        return {'User-Agent': f'CoveoSDKPython/{self.version}'}
