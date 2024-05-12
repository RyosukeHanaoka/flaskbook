from datetime import datetime
from .extensions import db

class Labo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    crp = db.Column(db.Float, nullable=False)
    esr = db.Column(db.Integer, nullable=False)
    rf = db.Column(db.Float, nullable=False)
    acpa = db.Column(db.Float, nullable=False)