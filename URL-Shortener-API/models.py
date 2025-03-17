from config import db
import datetime

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    short_code = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    access_count = db.Column(db.Integer, default=0)
    
    def to_json(self, include_access_count=False):
        data = {
            'id': self.id,
            'url': self.url,
            'shortCode': self.short_code,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at,
        }
        if include_access_count:
            data['accessCount'] = self.access_count
        return data
