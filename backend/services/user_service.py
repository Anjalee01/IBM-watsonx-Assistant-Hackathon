from models.user import User, db
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta

class UserService:
    """Service class for managing users."""

    @staticmethod
    def register_user(username, email, password):
        """Register a new user."""
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists.")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists.")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        """Authenticate a user and return a JWT token."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user.generate_auth_token()
        raise ValueError("Invalid username or password.")

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, username=None, email=None, password=None):
        """Update user information."""
        user = User.query.get(user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)
            db.session.commit()
            return user
        raise ValueError("User not found.")

    @staticmethod
    def delete_user(user_id):
        """Delete a user by their ID."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        raise ValueError("User not found.")
