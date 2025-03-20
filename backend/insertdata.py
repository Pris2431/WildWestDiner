from astrapy import DataAPIClient
import datetime
import uuid
import json  

# Initialize Astra DB client
client = DataAPIClient("AstraCS:sUIfhNWnqJEEMaAOXrHPyzBw:ed499a00a607a6e35eb0a38093cda4b3e824eeff5387ce71a5068caabc5fdfc4")
db = client.get_database_by_api_endpoint(
    "https://fe95d1a2-a484-4582-87c8-eed63d0104e0-us-east1.apps.astra.datastax.com",
    keyspace="orders_keyspace",
)

# Correct Collection Access
orders_collection = db.get_collection("orders")

# Get the latest order number
latest_order = orders_collection.find_one(sort={"order_number": -1})
next_order_number = (latest_order["order_number"] + 1) if latest_order else 1  # Increment order number

# Order Data
order_data = {
    "order_id": str(uuid.uuid4()),
    "order_number": next_order_number,
    "table_name": "Table 2",
    "order_time": datetime.datetime.now(datetime.timezone.utc),  # Full datetime object
    "items": json.dumps([  # Convert list to JSON string
        {"name": "Fish and Chips", "quantity": 1, "status": "waiting"},
        {"name": "Spaghetti Bolognese", "quantity": 2, "status": "waiting"},
        {"name": "Stuffed Mushrooms", "quantity": 2, "status": "waiting"},
        {"name": "Lamb Chop", "quantity": 2, "status": "waiting"},
        {"name": "Cheese Platter", "quantity": 2, "status": "waiting"},
    ]),
}

# Insert into AstraDB
orders_collection.insert_one(order_data)

print(f"Order #{str(next_order_number).zfill(4)} inserted successfully!")
