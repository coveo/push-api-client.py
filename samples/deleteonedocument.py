from push_api_clientpy import Source

source = Source("my_api_key", "my_org_id")
response = source.deleteDocument("the_name_of_my_source", "https://foo.com", True)

print(f"Deleted document: {response.json()}")
