from models.order import Order, db

class OrderService:
    """Service class for managing orders."""

    @staticmethod
    def get_all_orders(user_id=None):
        """Retrieve all orders or orders for a specific user."""
        if user_id:
            return Order.query.filter_by(user_id=user_id).all()
        return Order.query.all()

    @staticmethod
    def get_order(order_id):
        """Retrieve a specific order by its ID."""
        return Order.query.filter_by(order_id=order_id).first()

    @staticmethod
    def create_order(order_data):
        """Create a new order."""
        new_order = Order(
            order_id=order_data['order_id'],
            user_id=order_data['user_id'],
            status=order_data['status'],
            total_amount=order_data['total_amount'],
            description=order_data['description'],
            tracking=order_data['tracking']
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update_order(order_id, update_data):
        """Update an existing order."""
        order = Order.query.filter_by(order_id=order_id).first()
        if order:
            order.status = update_data.get('status', order.status)
            order.total_amount = update_data.get('total_amount', order.total_amount)
            order.description = update_data.get('description', order.description)
            order.tracking = update_data.get('tracking', order.tracking)
            db.session.commit()
            return order
        return None

    @staticmethod
    def delete_order(order_id):
        """Delete an order by its ID."""
        order = Order.query.filter_by(order_id=order_id).first()
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
