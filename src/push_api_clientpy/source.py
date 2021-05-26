from .platformclient import PlatformClient, SecurityIdentityAliasModel, SecurityIdentityBatchConfig, SecurityIdentityDelete, SecurityIdentityDeleteOptions, SecurityIdentityModel, SourceVisibility
from .documentbuilder import DocumentBuilder

class Source:
    def __init__(self, apikey: str, organizationid: str):
        self.client = PlatformClient(apikey, organizationid)

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
