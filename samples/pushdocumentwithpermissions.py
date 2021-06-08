from push_api_clientpy import Source, DocumentBuilder, UserSecurityIdentityBuilder

source = Source("my_api_key", "my_org_id")

allowedUsers = UserSecurityIdentityBuilder(["bob@sample.com", "john@sample.com"])

deniedUsers = UserSecurityIdentityBuilder(["jane@sample.com", "jack@sample.com"])

myDocument = DocumentBuilder("https://my.document.uri", "My document title")\
    .withAllowAnonymousUsers(False)\
    .withAllowedPermissions(allowedUsers)\
    .withDeniedPermissions(deniedUsers)

response = source.addOrUpdateDocument("my_source_id", myDocument)

print(f"Document added: {response.json()}")
