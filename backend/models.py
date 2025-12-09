from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

# Define models for Flask-Security

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Helper handle hash
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) # Required by FS
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    decks = db.relationship('Deck', backref='author', lazy=True)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cards = db.relationship('Card', backref='deck', lazy=True, cascade="all, delete-orphan")

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # SRS fields
    next_review = db.Column(db.DateTime, default=datetime.utcnow)
    interval = db.Column(db.Float, default=0.0)
    ease_factor = db.Column(db.Float, default=2.5)
    repetition = db.Column(db.Integer, default=0)

class ReviewLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 0-5
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)
