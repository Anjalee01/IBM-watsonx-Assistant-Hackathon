from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        return jwt.encode(
            {'id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expiration)},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return None
        return User.query.get(data['id'])

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    tracking = db.Column(db.JSON, nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        user = User.verify_auth_token(token)
        if not user:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        abort(400, 'Invalid request data')

    user = User.query.filter_by(username=data['username']).first()
    if user:
        abort(400, 'Username already exists')

    user = User.query.filter_by(email=data['email']).first()
    if user:
        abort(400, 'Email already exists')

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, 'Invalid request data')

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        abort(401, 'Invalid username or password')

    token = user.generate_auth_token()
    return jsonify({'token': token.decode('utf-8')})

@app.route('/orders', methods=['GET'])
@token_required
def get_orders(user):
    orders = user.orders.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/orders/<order_id>', methods=['GET'])
@token_required
def get_order(user, order_id):
    order = Order.query.filter_by(order_id=order_id, user_id=user.id).first()
    if not order:
        abort(404, 'Order not found')
    return jsonify(order.to_dict())

@app.route('/orders', methods=['POST'])
@token_required
def create_order(user):
    data = request.get_json()
    if not data or 'order_id' not in data or 'status' not in data or 'total_amount' not in data or 'description' not in data or 'tracking' not in data:
        abort(400, 'Invalid request data')

    order = Order(
        order_id=data['order_id'],
        user_id=user.id,
        status=data['status'],
        total_amount=data['total_amount'],
        description=data['description'],
        tracking=data['tracking']
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@app.route('/orders/<order_id>', methods=['PUT'])
@token_required
def update_order(user, order_id):
    order = Order.query.filter_by(order_id=order_id, user_id=user.id).first()
    if not order:
        abort(404, 'Order not found')

    data = request.get_json()
    if not data:
        abort(400, 'Invalid request data')

    order.status = data.get('status', order.status)
    order.total_amount = data.get('total_amount', order.total_amount)
    order.description = data.get('description', order.description)
    order.tracking = data.get('tracking', order.tracking)
    db.session.commit()
    return jsonify(order.to_dict())

@app.route('/orders/<order_id>', methods=['DELETE'])
@token_required
def delete_order(user, order_id):
    order = Order.query.filter_by(order_id=order_id, user_id=user.id).first()
    if not order:
        abort(404, 'Order not found')

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
