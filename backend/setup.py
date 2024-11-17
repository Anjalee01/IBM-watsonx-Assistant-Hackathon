from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Sample data for orders
orders = [
    {
        "orderId": "order123",
        "userId": "user123",
        "status": "Delivered",
        "totalAmount": 70.0,
        "description": "Order of electronics",
        "tracking": {
            "carrier": "FedEx",
            "currentStatus": "Delivered",
            "trackingNumber": "FEDEX123456789",
            "estimatedDeliveryDate": "2024-10-18T15:00:00Z"
        }
    },
    {
        "orderId": "order124",
        "userId": "user456",
        "status": "In Transit",
        "totalAmount": 120.0,
        "description": "Order of home appliances",
        "tracking": {
            "carrier": "UPS",
            "currentStatus": "Out for delivery",
            "trackingNumber": "UPS987654321",
            "estimatedDeliveryDate": "2024-10-20T12:00:00Z"
        }
    }
]

# Sample user data
users = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob", "email": "bob@example.com"}
}

# Contact support information
contact_support = {
    "supportEmail": "support@ecommerceplatform.com",
    "supportPhone": "+1-800-555-1234",
    "liveChatAvailable": True
}

@app.route('/api/orders/', methods=['GET'])
def get_orders():
    """Retrieve the list of orders."""
    user_id = request.args.get('userId')
    if user_id:
        user_orders = [order for order in orders if order['userId'] == user_id]
        logging.info(f"Retrieved orders for user {user_id}: {user_orders}")
        return jsonify(user_orders)
    logging.info("Retrieved all orders.")
    return jsonify(orders)

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve a specific order by its ID."""
    order = next((order for order in orders if order["orderId"] == order_id), None)
    if order is None:
        abort(404, description="Order not found.")
    logging.info(f"Retrieved order {order_id}: {order}")
    return jsonify(order)

@app.route('/api/support/', methods=['GET'])
def get_support_info():
    """Retrieve contact support information."""
    logging.info("Retrieved support information.")
    return jsonify(contact_support)

@app.route('/api/orders/', methods=['POST'])
def create_order():
    """Create a new order."""
    if not request.json or 'orderId' not in request.json:
        abort(400, description="Invalid order data.")
    
    new_order = {
        "orderId": request.json['orderId'],
        "userId": request.json['userId'],
        "status": "Processing",
        "totalAmount": request.json.get('totalAmount', 0.0),
        "description": request.json.get('description', ""),
        "tracking": {
            "carrier": request.json.get('carrier', ""),
            "currentStatus": "Processing",
            "trackingNumber": request.json.get('trackingNumber', ""),
            "estimatedDeliveryDate": request.json.get('estimatedDeliveryDate', "")
        }
    }
    orders.append(new_order)
    logging.info(f"Created new order: {new_order}")
    return jsonify(new_order), 201

@app.route('/api/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an existing order."""
    order = next((order for order in orders if order["orderId"] == order_id), None)
    if order is None:
        abort(404, description="Order not found.")
    
    if not request.json:
        abort(400, description="Invalid order data.")

    order['status'] = request.json.get('status', order['status'])
    order['totalAmount'] = request.json.get('totalAmount', order['totalAmount'])
    order['description'] = request.json.get('description', order['description'])
    
    if 'tracking' in request.json:
        order['tracking'].update(request.json['tracking'])
    
    logging.info(f"Updated order {order_id}: {order}")
    return jsonify(order)

@app.route('/api/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order by its ID."""
    global orders
    orders = [order for order in orders if order["orderId"] != order_id]
    logging.info(f"Deleted order {order_id}.")
    return jsonify({"result": True})

@app.route('/api/users/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    """Retrieve all orders for a specific user."""
    user_orders = [order for order in orders if order['userId'] == user_id]
    if not user_orders:
        abort(404, description="No orders found for this user.")
    logging.info(f"Retrieved orders for user {user_id}: {user_orders}")
    return jsonify(user_orders)

@app.route('/api/users/', methods=['POST'])
def create_user():
    """Create a new user."""
    if not request.json or 'userId' not in request.json:
        abort(400, description="Invalid user data.")
    
    new_user = {
        "userId": request.json['userId'],
        "name": request.json.get('name', ""),
        "email": request.json.get('email', "")
    }
    users[new_user['userId']] = new_user
    logging.info(f"Created new user: {new_user}")
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
