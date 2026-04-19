from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(150), unique=True, nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password      = db.Column(db.String(300), nullable=False)   # scrypt hash
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    # Brute-force protection fields
    failed_logins = db.Column(db.Integer, default=0, nullable=False)
    locked_until  = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'students'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    student_code  = db.Column(db.String(50), unique=True, nullable=False)
    email         = db.Column(db.String(150), nullable=False)
    course        = db.Column(db.String(100), nullable=False)
    year          = db.Column(db.String(50), nullable=True)
    date_created  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name}>'
