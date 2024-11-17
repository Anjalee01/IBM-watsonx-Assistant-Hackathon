from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    """Order model for tracking orders in the system."""
    
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    tracking = db.Column(db.JSON, nullable=False)

    # Relationships
    user = db.relationship('User', backref='orders')

    def to_dict(self):
        """Convert the order object to a dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'description': self.description,
            'tracking': self.tracking
        }
