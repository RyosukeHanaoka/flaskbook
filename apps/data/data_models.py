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
    immunology_score = db.Column(db.Integer, nullable=False)
    inflammation_score = db.Column(db.Integer, nullable=False)


def immunology_score(rf, acpa):
    immunology_score = 0  # 免疫学的スコアの初期値を設定
    # 最初の条件群
    if rf >= 45:
        return 2
    elif acpa >= 13.5:
        return 2
    elif rf >= 15:
        return 1
    elif acpa >= 4.5:
        return 1
    else:
        return 0

def inflammation_score(crp, esr, sex):
    # crpとesrの値によってスコアを返す
    if crp > 0.3:
        return 1
    elif sex == 0:
        if esr > 10:
            return 1
        else:
            return 0
    elif sex == 1:
        if esr > 15:
            return 1
        return 0