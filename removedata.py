from astrapy import DataAPIClient
import json  

# Initialize Astra DB client
client = DataAPIClient("AstraCS:sUIfhNWnqJEEMaAOXrHPyzBw:ed499a00a607a6e35eb0a38093cda4b3e824eeff5387ce71a5068caabc5fdfc4")
db = client.get_database_by_api_endpoint(
    "https://fe95d1a2-a484-4582-87c8-eed63d0104e0-us-east1.apps.astra.datastax.com",
    keyspace="orders_keyspace",
)

# Correct Collection Access
orders_collection = db.get_collection("orders")

# UUID of the order to delete (replace with the actual UUID)
order_id_to_delete = "756d2ba7-2e90-4d4c-94a6-3424446e2d99"

# Delete the order
result = orders_collection.delete_one({"order_id": order_id_to_delete})

if result.deleted_count > 0:
    print(f"Order with ID {order_id_to_delete} deleted successfully!")
else:
    print(f"Order with ID {order_id_to_delete} not found.")
