from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:sUIfhNWnqJEEMaAOXrHPyzBw:ed499a00a607a6e35eb0a38093cda4b3e824eeff5387ce71a5068caabc5fdfc4")
db = client.get_database_by_api_endpoint(
  "https://fe95d1a2-a484-4582-87c8-eed63d0104e0-us-east1.apps.astra.datastax.com",
    keyspace="orders_keyspace",
)
      
print(f"Connected to Astra DB: {db.list_collection_names()}")
