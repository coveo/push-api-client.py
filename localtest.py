
from src.push_api_clientpy import DocumentBuilder, Source, SecurityIdentityModel, IdentityModel, AliasMapping, SecurityIdentityAliasModel, SecurityIdentityDelete
import datetime
from dotenv import dotenv_values

docBuilder = DocumentBuilder('id', 'title')\
    .withDate(datetime.datetime.now())\
    .withModifiedDate("2000/01/01")\
    .withClickableUri('https://clicky.uri')\
    .withFileExtension('.html')\
    .withParentId('parent_id')\
    .withMetadata({"foo": "bar", "bar": ["buzz"]})\
    .withMetadataValue("hello", [1, 2, 3])

print(docBuilder.marshal())

source = Source(apikey=dotenv_values().get("API_KEY"),
                organizationid=dotenv_values().get("ORG_ID"))

createSourceResponse = source.create('testlocalpython', "SECURED")
print(createSourceResponse.status_code, createSourceResponse.json())

identityModel = IdentityModel(
    AdditionalInfo={"foo": "bar"},
    Name="the_security_identity_name",
    Type="USER"
)

securityIdentityModel = SecurityIdentityModel(
    Identity=identityModel,
    WellKnowns=[identityModel],
    Members=[identityModel]
)

createSecurityIdentityResponse = source.createOrUpdateSecurityIdentity(
    "Email Security Provider", securityIdentityModel)

print(createSecurityIdentityResponse.status_code, createSecurityIdentityResponse.json())

mapping = AliasMapping(
    AdditionalInfo=identityModel.AdditionalInfo,
    Name=identityModel.Name,
    Type=identityModel.Type,
    Provider="Email Security Provider"
)
alias = SecurityIdentityAliasModel(
    Identity=identityModel,
    WellKnowns=[identityModel],
    Mappings=[mapping])

createAliasResponse = source.createOrUpdateSecurityIdentityAlias(
    "Email Security Provider", alias)
print(createAliasResponse.status_code, createAliasResponse.json())

delete = SecurityIdentityDelete(identityModel)
deleteIdentityResponse = source.deleteSecurityIdentity(
    "Email Security Provider",
    delete
)
print(deleteIdentityResponse.status_code, deleteIdentityResponse.json())

