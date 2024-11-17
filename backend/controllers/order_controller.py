from flask import Blueprint, jsonify, request, abort
from models.order import Order
from models.user import User, db
from services.order_service import OrderService

order_bp = Blueprint('order', __name__)

@order_bp.route('/api/orders/', methods=['GET'])
def get_orders():
    """Retrieve all orders or orders for a specific user."""
    user_id = request.args.get('userId')
    orders = OrderService.get_all_orders(user_id)
    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route('/api/orders/', methods=['POST'])
def create_order():
    """Create a new order."""
    order_data = request.get_json()
    new_order = OrderService.create_order(order_data)
    return jsonify(new_order.to_dict()), 201

# Similar changes can be made for update_order and delete_order endpoints.

@order_bp.route('/api/orders/', methods=['GET'])
def get_orders():
    """Retrieve all orders or orders for a specific user."""
    user_id = request.args.get('userId')
    if user_id:
        user_orders = Order.query.filter_by(user_id=user_id).all()
        if not user_orders:
            return jsonify([]), 200
        return jsonify([order.to_dict() for order in user_orders]), 200
    all_orders = Order.query.all()
    return jsonify([order.to_dict() for order in all_orders]), 200

@order_bp.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve a specific order by its ID."""
    order = Order.query.filter_by(order_id=order_id).first()
    if order is None:
        abort(404, description="Order not found.")
    return jsonify(order.to_dict()), 200

@order_bp.route('/api/orders/', methods=['POST'])
def create_order():
    """Create a new order."""
    if not request.json:
        abort(400, description="Invalid order data.")
    
    required_fields = ['order_id', 'user_id', 'status', 'total_amount', 'description', 'tracking']
    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"{field} is required.")

    new_order = Order(
        order_id=request.json['order_id'],
        user_id=request.json['user_id'],
        status=request.json['status'],
        total_amount=request.json['total_amount'],
        description=request.json['description'],
        tracking=request.json['tracking']
    )
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify(new_order.to_dict()), 201

@order_bp.route('/api/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an existing order."""
    order = Order.query.filter_by(order_id=order_id).first()
    if order is None:
        abort(404, description="Order not found.")

    if not request.json:
        abort(400, description="Invalid order data.")

    order.status = request.json.get('status', order.status)
    order.total_amount = request.json.get('total_amount', order.total_amount)
    order.description = request.json.get('description', order.description)
    order.tracking = request.json.get('tracking', order.tracking)
    
    db.session.commit()
    return jsonify(order.to_dict()), 200

@order_bp.route('/api/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order by its ID."""
    order = Order.query.filter_by(order_id=order_id).first()
    if order is None:
        abort(404, description="Order not found.")

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully.'}), 200
