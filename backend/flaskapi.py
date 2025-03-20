from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from statusupdates import update_order_status

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Set up Flask-SocketIO
socketio = SocketIO(app)

# In-memory list of orders (you can replace this with a database)
orders = [
    {"id": 1, "items": [{"name": "Pizza", "status": "pending"}]},
    {"id": 2, "items": [{"name": "Pasta", "status": "pending"}]},
]

@app.route("/update-status", methods=["POST"])
def update_status():
    data = request.json
    order_id = data["orderId"]
    item_index = data["itemIndex"]
    new_status = data["status"]

    # Update the order status (you can call your function here if necessary)
    update_order_status(order_id, item_index, new_status)

    # Find the order and update item status in the in-memory list
    for order in orders:
        if order["id"] == order_id:
            order["items"][item_index]["status"] = new_status
            break

    # Emit the updated order status to all clients
    socketio.emit("orderUpdate", {"orders": orders})

    return jsonify({"message": "Status updated successfully"}), 200

# SocketIO event to handle updates
@socketio.on("updateItemStatus")
def handle_update_item_status(data):
    order_id = data.get("orderId")
    item_index = data.get("itemIndex")
    new_status = data.get("status")
    
    # Find the order and update item status
    for order in orders:
        if order["id"] == order_id:
            order["items"][item_index]["status"] = new_status
            break

    # Broadcast updated orders to all clients
    socketio.emit("orderUpdate", {"orders": orders})

if __name__ == "__main__":
    # Run the app with SocketIO
    socketio.run(app, debug=True, port=5000)
