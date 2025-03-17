from config import db
from sqlalchemy import ForeignKey


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    hash = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(32), nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.name}"
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'hash': self.hash
        }
        
        
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        return f"Todo List('{self.title}', '{self.description})"
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }