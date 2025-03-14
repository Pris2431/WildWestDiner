from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
from astrapy import DataAPIClient
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for WebSocket

# AstraDB connection
client = DataAPIClient("AstraCS:sUIfhNWnqJEEMaAOXrHPyzBw:ed499a00a607a6e35eb0a38093cda4b3e824eeff5387ce71a5068caabc5fdfc4")
db = client.get_database_by_api_endpoint(
    "https://fe95d1a2-a484-4582-87c8-eed63d0104e0-us-east1.apps.astra.datastax.com",
    keyspace="orders_keyspace",
)
orders_collection = db.get_collection("orders", keyspace="orders_keyspace")
print(f"Connected to Astra DB: {db.list_collection_names()}")

@socketio.on('connect')
def handle_connect():
    initial_orders = list(orders_collection.find({}))
    emit('initialOrders', {'orders': initial_orders})

@socketio.on('updateItemStatus')
def handle_item_status_update(data):
    updated_order = orders_collection.find_one({"order_id": data['orderId']})
    
    # Update specific item's status
    items = json.loads(updated_order['items'])
    items[data['itemIndex']]['status'] = data['newStatus']
    
    orders_collection.update_one(
        {"order_id": data['orderId']},
        {"$set": {"items": json.dumps(items)}}
    )
    
    # Broadcast update to all clients
    emit('orderStatusUpdate', {'order': updated_order}, broadcast=True)

@socketio.on('deleteOrder')
def handle_delete_order(data):
    order_uuid = data.get('orderUuid')
    if order_uuid:
        try:
            print(f"Attempting to delete order: {order_uuid}")
            # Perform your deletion logic
            result = orders_collection.delete_one({"order_uuid": order_uuid})
            
            if result.deleted_count > 0:
                print(f"Deleted order {order_uuid}")
                socketio.emit('orderDeleted', {'orderUuid': order_uuid}, broadcast=True)
            else:
                print(f"No order found with UUID {order_uuid}")
                emit('error', {'message': 'Order not found in database'})
        except Exception as e:
            print(f"Deletion error: {str(e)}")
            emit('error', {'message': 'Database error occurred'})
    else:
        print("No orderUuid received")
        emit('error', {'message': 'Order UUID not provided'})

# Handle OPTIONS requests for CORS preflight
@app.route("/", methods=["OPTIONS"])
def handle_options():
    return "", 200  # Return an empty response with 200 OK

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
