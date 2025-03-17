from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


def create_short_code():
    chars = string.ascii_letters + string.digits
    
    s = ''.join(random.choice(chars) for _ in range(8))
    return s