from push_api_clientpy import Source

source = Source("my_api_key", "my_org_id")
response = source.create("the_name_of_my_source", "SECURED")

print(f'Successfully created source: {response.json()}')