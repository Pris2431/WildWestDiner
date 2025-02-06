import json
from orders import orders

# Transform orders into JavaScript-compatible format
orders_js_data = []

for order in orders:
    items = json.loads(order['items'])  # Ensure items are in list format
    js_order = {
        "id": order["order_id"],
        "table": order["table_name"],
        "time": order["order_time"],
        "items": [
            {
                "name": item["name"],
                "quantity": item["quantity"],
                "status": item["status"]
            }
            for item in items
        ]
    }
    orders_js_data.append(js_order)

# Convert to JavaScript format
js_content = f"const currentOrders = {json.dumps(orders_js_data, indent=4)};"

# Save as orders.js
with open("orders.js", "w") as f:
    f.write(js_content)

print("JavaScript file generated: orders.js")
