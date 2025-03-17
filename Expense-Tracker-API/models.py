from config import db
import datetime
from sqlalchemy import ForeignKey

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    
    
    def __repr__(self):
        return f'User: {self.id}, {self.name}'
    
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
        
        
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'amount': self.amount,
            'date': self.created_at
        }
    