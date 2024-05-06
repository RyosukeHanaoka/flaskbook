from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"
    #ユーザーのID (主キー)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #ユーザーのメールアドレス (一意制約、非Null制約)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #ハッシュ化されたパスワード
    password_hash = db.Column(db.String(128))
    #ユーザーが作成された日時
    created_at = db.Column(db.DateTime, default=datetime.now)
    #ユーザーが最後に更新された日時
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    #与えられたパスワードをハッシュ化してpassword_hash属性に設定
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #与えられたパスワードが、保存されているハッシュ値と一致するかチェック
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    #ユーザーIDを文字列として返す (Flask-Loginで必要)
    def get_id(self):
        return str(self.id)
    #ユーザーを表す文字列表現を返す
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sex = db.Column(db.String(10))
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    onset_year = db.Column(db.Integer)
    onset_month = db.Column(db.Integer)
    onset_day = db.Column(db.Integer)
    morning_stiffness = db.Column(db.String(50))
    stiffness_duration = db.Column(db.Integer)
    pain_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def calculate_age(self, current_year, current_month, current_day):
        age = current_year - self.birth_year
        if (current_month, current_day) < (self.birth_month, self.birth_day):
            age -= 1
        return age    
    
def joint_score(proximal_joints, distal_joints):
    joint_score = 0  # 関節スコアの初期値を設定
    # "distal_joints"が0のときの条件
    if distal_joints == 0:
        if proximal_joints == 0:
            return 0
        else:
            return 1
    # distal_jointsが0より大きい数のときの条件
    else:
        # proximal_joints + distal_jointsの合計が11以上の場合
        if proximal_joints + distal_joints >= 11:
            return 5
        # proximal_joints + distal_jointsの合計が10未満の場合
        elif proximal_joints + distal_joints < 10:
        # distal_jointsが3以下の場合
            if distal_joints <= 3:
                return 2
        # distal_jointsが4以上の場合
            else:
                return 3


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