from datetime import datetime
import hashlib
from push_api_clientpy import DocumentBuilder, UserSecurityIdentityBuilder
import pytest


@pytest.fixture
def docBuilder():
    return DocumentBuilder("https://foo.com", "title")


@pytest.fixture
def bob():
    return UserSecurityIdentityBuilder("bob@acme.inc")


@pytest.fixture
def alice():
    return UserSecurityIdentityBuilder("alice@acme.inc")


@pytest.fixture
def multiple():
    return UserSecurityIdentityBuilder(["bob@acme.inc", "alice@acme.inc"])


class TestDocBuilder:

    def testMarshalDocumentId(self, docBuilder):
        assert docBuilder.marshal().get("documentId") == "https://foo.com"

    def testMarshalDocumentTitle(self, docBuilder):
        assert docBuilder.marshal().get("title") == "title"

    def testMarshalDocumentData(self, docBuilder):
        assert docBuilder.withData("the data").marshal().get("data") == "the data"

    def testMarshalDocumentCompressedBinaryData(self, docBuilder):
        docBuilder.withCompressedBinaryData("the data compressed", "UNCOMPRESSED")
        assert docBuilder.marshal().get("compressedBinaryData") == "the data compressed"
        assert docBuilder.marshal().get("compressionType") == "UNCOMPRESSED"

    def testMarshalDocumentDateAsString(self, docBuilder):
        docBuilder.withDate("2000/01/01")
        assert docBuilder.marshal().get("date") == "2000-01-01T00:00:00"

    def testMarshalDocumentDateAsNumber(self, docBuilder):
        docBuilder.withDate(1262322000)
        assert docBuilder.marshal().get("date") == datetime.fromtimestamp(1262322000).isoformat()

    def testMarshalDocumentDateAsDatetime(self, docBuilder):
        docBuilder.withDate(datetime.fromtimestamp(1577854800))
        assert docBuilder.marshal().get("date") == datetime.fromtimestamp(1577854800).isoformat()

    def testMarshalDocumentModifiedDateAsString(self, docBuilder):
        docBuilder.withModifiedDate("2000/01/01")
        assert docBuilder.marshal().get("modifiedDate") == "2000-01-01T00:00:00"

    def testMarshalDocumentModifiedDateAsNumber(self, docBuilder):
        docBuilder.withModifiedDate(1262322000)
        assert docBuilder.marshal().get("modifiedDate") == datetime.fromtimestamp(1262322000).isoformat()

    def testMarshalDocumentModifiedDateAsDatetime(self, docBuilder):
        docBuilder.withModifiedDate(datetime.fromtimestamp(1577854800))
        assert docBuilder.marshal().get("modifiedDate") == datetime.fromtimestamp(1577854800).isoformat()

    def testMarshalDocumentPermanentId(self, docBuilder):
        docBuilder.withPermanentId("the_id")
        assert docBuilder.marshal().get("permanentId") == "the_id"

    def testMarshalDocumentPermanentIdFromURI(self, docBuilder):
        # 'https://foo.com'
        assert docBuilder.marshal().get("permanentId") == 'aa2e0510b66edff7f05e2b30d4f1b3a4b5481c06b69f41751c54675c5afb'

    def testMarshalFileExtension(self, docBuilder):
        docBuilder.withFileExtension(".html")
        assert docBuilder.marshal().get("fileExtension") == ".html"

    def testMarshalParentId(self, docBuilder):
        docBuilder.withParentId("the_id")
        assert docBuilder.marshal().get("parentId") == "the_id"

    def testMarshalClickableUri(self, docBuilder):
        docBuilder.withClickableUri("https://the_click_uri.com")
        assert docBuilder.marshal().get("clickableUri") == "https://the_click_uri.com"

    def testMarshalMetadataValue(self, docBuilder):
        docBuilder.withMetadataValue("foo", "bar")
        assert docBuilder.marshal().get("foo") == "bar"
        assert docBuilder.marshal().get("metadata") is None

    def testMarshalMetadata(self, docBuilder):
        docBuilder.withMetadata({"foo": "bar", "buzz": "bazz"})
        assert docBuilder.marshal().get("foo") == "bar"
        assert docBuilder.marshal().get("buzz") == "bazz"
        assert docBuilder.marshal().get("metadata") is None

    def testMarshalAllowedPermissions(self, docBuilder, bob):
        docBuilder.withAllowedPermissions(bob)
        assert docBuilder.marshal().get("permissions")[0].get("allowedPermissions")[
            0].get("identity") == bob.identity

    def testMarshalMultipleAllowedPermissions(self, docBuilder, bob, alice, multiple):
        docBuilder.withAllowedPermissions(multiple)
        assert docBuilder.marshal().get("permissions")[0].get("allowedPermissions")[
            0].get("identity") == bob.identity
        assert docBuilder.marshal().get("permissions")[0].get("allowedPermissions")[
            1].get("identity") == alice.identity

    def testMarshalDeniedPermissions(self, docBuilder, bob):
        docBuilder.withDeniedPermissions(bob)
        assert docBuilder.marshal().get("permissions")[0].get("deniedPermissions")[
            0].get("identity") == bob.identity

    def testMarshalMultipleDeniedPermissions(self, docBuilder, bob, alice, multiple):
        docBuilder.withDeniedPermissions(multiple)
        assert docBuilder.marshal().get("permissions")[0].get("deniedPermissions")[
            0].get("identity") == bob.identity
        assert docBuilder.marshal().get("permissions")[0].get("deniedPermissions")[
            1].get("identity") == alice.identity

    def testMarshalAllowAnonymousUsersFalse(self, docBuilder):
        docBuilder.withAllowAnonymousUsers(False)
        assert docBuilder.marshal().get("permissions")[0].get("allowAnonymous") == False

    def testMarshalAllowAnonymousUsersTrue(self, docBuilder):
        docBuilder.withAllowAnonymousUsers(True)
        assert docBuilder.marshal().get("permissions")[0].get("allowAnonymous") == True

    def testMarshalAuthor(self, docBuilder):
        docBuilder.withAuthor("bob")
        assert docBuilder.marshal().get("author") == "bob"
