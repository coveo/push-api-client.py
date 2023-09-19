from .platformclient import BatchUpdateDocuments, FileContainer, PlatformClient, SecurityIdentityAliasModel, SecurityIdentityBatchConfig, SecurityIdentityDelete, SecurityIdentityDeleteOptions, SecurityIdentityModel, SourceVisibility, DEFAULT_MAX_RETRIES, DEFAULT_RETRY_AFTER
from .platformclient import BackoffOptions
from .documentbuilder import DocumentBuilder
from dataclasses import asdict, dataclass
import json


@dataclass
class BatchUpdate(BatchUpdateDocuments):
    addOrUpdate: list[DocumentBuilder]


class Source:
    def __init__(self, apikey: str, organizationid: str, backoff_options: BackoffOptions = BackoffOptions()):
        self.client = PlatformClient(apikey, organizationid, backoff_options)

    def create(self, name: str, visibility: SourceVisibility):
        return self.client.createSource(name, visibility)

    def createOrUpdateSecurityIdentity(self, securityProviderId: str, securityIdentityModel: SecurityIdentityModel):
        return self.client.createOrUpdateSecurityIdentity(securityProviderId, securityIdentityModel)

    def createOrUpdateSecurityIdentityAlias(self, securityProviderId: str, securityIdentityAlias: SecurityIdentityAliasModel):
        return self.client.createOrUpdateSecurityIdentityAlias(securityProviderId, securityIdentityAlias)

    def deleteSecurityIdentity(self, securityProviderId: str, securityIdentityToDelete: SecurityIdentityDelete):
        return self.client.deleteSecurityIdentity(securityProviderId, securityIdentityToDelete)

    def deleteOldSecurityIdentities(self, securityProviderId: str, batchDelete: SecurityIdentityDeleteOptions):
        return self.client.deleteOldSecurityIdentities(securityProviderId, batchDelete)

    def manageSecurityIdentities(self, securityProviderId: str, batchConfig: SecurityIdentityBatchConfig):
        return self.client.manageSecurityIdentities(securityProviderId, batchConfig)

    def addOrUpdateDocument(self, sourceId: str, docBuilder: DocumentBuilder):
        return self.client.pushDocument(sourceId, docBuilder.marshal())

    def deleteDocument(self, sourceId: str, documentId: str):
        return self.client.deleteDocument(sourceId, documentId)

    def batchUpdateDocuments(self, sourceId: str, batch: BatchUpdate):
        resFileContainer = self.client.createFileContainer().json()

        fileContainer = FileContainer(
            uploadUri=resFileContainer.get('uploadUri'),
            fileId=resFileContainer.get('fileId'),
            requiredHeaders=resFileContainer.get('requiredHeaders'))

        batchMarshaled = BatchUpdateDocuments(
            addOrUpdate=list(
                map(lambda docBuilder: docBuilder.marshal(), batch.addOrUpdate)),
            delete=batch.delete)

        self.client.uploadContentToFileContainer(fileContainer, batchMarshaled)

        return self.client.pushFileContainerContent(sourceId, fileContainer)
