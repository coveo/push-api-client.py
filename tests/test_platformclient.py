import pytest
from push_api_clientpy import IdentityModel, PlatformClient, SecurityIdentityModel, SecurityIdentityAliasModel, AliasMapping, SecurityIdentityDelete, DocumentBuilder, BatchDelete, BatchUpdateDocuments, FileContainer, SecurityIdentityBatchConfig, BackoffOptions


@pytest.fixture
def client():
    return PlatformClient("my_key", "my_org", BackoffOptions(retry_after=100))


@pytest.fixture
def identityModel():
    return IdentityModel(AdditionalInfo={"foo": "bar"}, Name="the_name", Type="USER")


@pytest.fixture
def securityIdentityModel(identityModel):
    return SecurityIdentityModel(Identity=identityModel, WellKnowns=[identityModel], Members=[identityModel])


@pytest.fixture
def securityIdentityModelAlias(identityModel):
    return SecurityIdentityAliasModel(Identity=identityModel, WellKnowns=[identityModel], Mappings=[AliasMapping(AdditionalInfo=identityModel.AdditionalInfo, Name=identityModel.Name, Type=identityModel.Type, Provider="my_provider")])


@pytest.fixture
def securityIdentityDelete(identityModel):
    return SecurityIdentityDelete(Identity=identityModel)

@pytest.fixture
def securityIdentityBatchConfig():
    return SecurityIdentityBatchConfig(FileID="the_file_id", OrderingID=123)


@pytest.fixture
def fileContainer():
    return FileContainer(uploadUri="https://the.upload.uri", fileId="the_file_id", requiredHeaders={"foo": "bar"})


@pytest.fixture
def doc():
    return DocumentBuilder("http://foo.com", "the_title").marshal()

def assertAuthHeader(adapter):
    lastRequestHeaders = adapter.last_request.headers
    assert lastRequestHeaders.get("Authorization") == "Bearer my_key"


def assertContentTypeHeaders(adapter):
    lastRequestHeaders = adapter.last_request.headers
    assert lastRequestHeaders.get("Content-Type") == "application/json"
    assert lastRequestHeaders.get("Accept") == "application/json"


class TestPlatformClient:

    def testCreateSource(self, client, requests_mock):
        adapter = requests_mock.post(
            "https://platform.cloud.coveo.com/rest/organizations/my_org/sources", json={})
        client.createSource("my_source", "SHARED")
        lastRequestBody = adapter.last_request.json()

        assert lastRequestBody.get("sourceType") == "PUSH"
        assert lastRequestBody.get("pushEnabled") == True
        assert lastRequestBody.get("name") == "my_source"
        assert lastRequestBody.get("sourceVisibility") == "SHARED"

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testCreateOrUpdateSecurityIdentity(self, client, requests_mock, securityIdentityModel):
        adapter = requests_mock.put(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/providers/my_provider/permissions", json={})
        client.createOrUpdateSecurityIdentity("my_provider", securityIdentityModel)
        lastRequestBody = adapter.last_request.json()

        assert lastRequestBody.get("members")[0].get(
            "additionalInfo").get("foo") == "bar"
        assert lastRequestBody.get("members")[0].get("type") == "USER"

        assert lastRequestBody.get("wellKnowns")[0].get(
            "additionalInfo").get("foo") == "bar"
        assert lastRequestBody.get("wellKnowns")[0].get("type") == "USER"

        assert lastRequestBody.get("identity").get("name") == "the_name"

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testCreateOrUpdateSecurityIdentityAlias(self, client, requests_mock, securityIdentityModelAlias):
        adapter = requests_mock.put(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/providers/my_provider/mappings", json={})
        client.createOrUpdateSecurityIdentityAlias(
            "my_provider", securityIdentityModelAlias)
        lastRequestBody = adapter.last_request.json()

        assert lastRequestBody.get("mappings")[0].get(
            "additionalInfo").get("foo") == "bar"
        assert lastRequestBody.get("mappings")[0].get("type") == "USER"

        assert lastRequestBody.get("wellKnowns")[0].get(
            "additionalInfo").get("foo") == "bar"
        assert lastRequestBody.get("wellKnowns")[0].get("type") == "USER"

        assert lastRequestBody.get("identity").get("name") == "the_name"

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testDeleteSecurityIdentity(self, client, requests_mock, securityIdentityDelete):
        adapter = requests_mock.delete(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/providers/my_provider/permissions", json={})
        client.deleteSecurityIdentity(
            "my_provider", securityIdentityDelete)
        lastRequestBody = adapter.last_request.json()

        assert lastRequestBody.get("identity").get("name") == "the_name"

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testManageSecurityIdentities(self, client, requests_mock, securityIdentityBatchConfig):
        adapter = requests_mock.put(
            f"https://api.cloud.coveo.com/push/v1/organizations/my_org/providers/my_provider/permissions/batch?fileId={securityIdentityBatchConfig.FileID}&orderingId={securityIdentityBatchConfig.OrderingID}", json={})
        client.manageSecurityIdentities(
            "my_provider", securityIdentityBatchConfig)
        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testPushDocument(self, client, requests_mock, doc):
        adapter = requests_mock.put(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/sources/my_source/documents?documentId=http%3A%2F%2Ffoo.com")
        client.pushDocument("my_source", doc)

        lastRequestBody = adapter.last_request.json()

        assert lastRequestBody.get("title") == "the_title"

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testCreateFileContainer(self, client, requests_mock):
        adapter = requests_mock.post(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/files")
        client.createFileContainer()

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testUploadContentToFileContainer(self, client, requests_mock, fileContainer, doc):
        adapter = requests_mock.put(fileContainer.uploadUri)

        client.uploadContentToFileContainer(fileContainer, BatchUpdateDocuments(
            addOrUpdate=[doc], delete=[BatchDelete(documentId="the_id_to_delete", deleteChildren=True)]))

        lastRequestHeaders = adapter.last_request.headers
        lastRequestBody = adapter.last_request.json()
        for k, v in fileContainer.requiredHeaders.items():
            assert lastRequestHeaders.get(k) == v
        assert lastRequestBody.get("addOrUpdate")[0].get("title") == "the_title"
        assert lastRequestBody.get("delete")[0].get("documentId") == "the_id_to_delete"

    def testPushFileContainerContent(self, client, requests_mock, fileContainer):
        adapter = requests_mock.put(
            f"https://api.cloud.coveo.com/push/v1/organizations/my_org/sources/my_source/documents/batch?fileId={fileContainer.fileId}")

        client.pushFileContainerContent("my_source", fileContainer)

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testDeleteDocument(self, client, requests_mock):
        adapter = requests_mock.delete(
            "https://api.cloud.coveo.com/push/v1/organizations/my_org/sources/my_source/documents?deleteChildren=true&documentId=http%3A%2F%2Ffoo.com")
        client.deleteDocument("my_source", "http://foo.com", True)

        assertAuthHeader(adapter)
        assertContentTypeHeaders(adapter)

    def testRetryMechanismOptions(self):
        new_client = PlatformClient("my_key", "my_org", BackoffOptions(retry_after=100, max_retries=10))

        retry = new_client.retries
        assert retry.total == 10
        assert retry.backoff_factor == 100
