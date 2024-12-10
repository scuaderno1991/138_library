# app/models.py
import hashlib, os
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(32), nullable=False)  # Store the salt value
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def set_password(self, password):
        # Generate a random salt value
        self.salt = os.urandom(16).hex()
        # Combine the password and salt, then hash
        password_salt = password + self.salt
        self.password_hash = hashlib.sha256(password_salt.encode('utf-8')).hexdigest()

    def check_password(self, password):
        # Combine the entered password with the stored salt, then hash
        password_salt = password + self.salt
        entered_password_hash = hashlib.sha256(password_salt.encode('utf-8')).hexdigest()
        # Check if the generated hash matches the stored hash
        return self.password_hash == entered_password_hash
    
    # Method for updating user information (for edit profile)
    def update_info(self, first_name, last_name, username, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.role = role
        db.session.commit()

    # Method to check if the user is authenticated
    def is_authenticated(self):
        return True
    
    # Method to check if the user is anonymous
    def is_anonymous(self):
        return False
    
    # Method to get the user's ID
    def get_id(self):
        return str(self.id)
    
    # String representation of the User object, useful for debugging
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    can_view_users = db.Column(db.Boolean, default=False)  # New column

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)