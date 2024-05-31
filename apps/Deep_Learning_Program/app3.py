# app.py の中で
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
#from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String #DBのテーブルの型をインポート
from sqlalchemy import desc
from sqlalchemy import select
#from flask_sqlalchemy_session import flask_scoped_session
import sys
import datetime
def make_age(date):
    date=[int(x) for x in date.split('-')]
    year,month,day=date
    today = datetime.date.today()
    birthday = datetime.date(year, month, day)
    return (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000
def func():
    return 100

#password_hash = generate_password_hash('your_password')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arthritis_detector_database.db'
db = SQLAlchemy(app)

from sqlalchemy.orm import sessionmaker
SessionClass = sessionmaker(db)
session = SessionClass()

#session = flask_scoped_session(session_factory, app)
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    gender =  db.Column(db.String(4))
class Spec(db.Model):
    __tablename__ = 'spec'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(128))
    birthday = db.Column(db.String(12))
    age=0
class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))
    symptom = db.Column(db.Integer)

'''
def psw():
    # ここで `user` はデータベースから取得したユーザーオブジェクトとします
    # そして `form_password` はログインフォームから送信されたパスワードとします
    user = User.query.filter_by(email='user_email').first()
    check = check_password_hash(user.password_hash, 'form_password')
    if check:
        # パスワードが一致する場合
        print("パスワードが一致します。")
    else:
        # パスワードが一致しない場合
        print("パスワードが一致しません。")
'''
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        print("GET")
        data = User.query.all()
        for d in data:
            print(d)
        user = User.query.filter_by(password_hash='pass').first()
        print(user)
        print(user.email)

    '''
    user = User.query.filter_by(email='user_email').first()
    check = check_password_hash(user.password_hash, 'form_password')
    if check:
        # パスワードが一致する場合
        print("パスワードが一致します。")
    else:
        # パスワードが一致しない場合
        print("パスワードが一致しません。")
    '''
    return render_template('index.html')

@app.route('/form', methods = ['GET', 'POST'])
def informed_consent():
    return render_template('form.html')

@app.route('/form1', methods=['GET', 'POST'])
def symptom():
    return render_template('form1.html')

@app.route('/form2', methods=['GET', 'POST'])
def sign():
    return render_template('form2.html')

@app.route('/person', methods=['GET', 'POST'])
def person():
    global data,data_,d
    #data=Users.query.join(Spec).filter(Users.email =='mail@mail.com', Spec.email=='mail@mail.com').one()
    #data = Users.query.filter(Users.email =='mail@mail.com')
    data = Users.query.join(Spec, Users.email==Spec.email).all()
    data=db.session.query(Users, Spec).join(Users, Users.email == Spec.email).all()
    data=calcAge(data,1)
    fields=[['email','password','gender'],['name','birthday','age']]
    data_=field(data,fields)
    return render_template('person.html',data=data_)
@app.route('/person2', methods=['GET', 'POST'])
def person2():
    global data,data_,d,age,ages
    '''
    age=db.session.query(Spec.email,Spec.birthday).all()
    age={x[0]:make_age(x[1]) for x in age}
    ages=db.session.query(User.email,Spec.birthday).join(Spec, Users.email == Spec.email).all()
    '''
    data=db.session.query(Users.email,Users.password, Spec.name,Spec.birthday).join(Users, Users.email == Spec.email).all()
    return render_template('person2.html',data=data)
@app.route('/person3', methods=['GET', 'POST'])
def person3():
    global data
    data=db.session.query(Users.email,Spec.name,Spec.birthday).join(Users, Users.email == Spec.email).all()
    data=[[x[0],x[1],x[2],make_age(x[2])] for x in data]
    return render_template('person2.html',data=data)
@app.route('/check', methods=['GET', 'POST'])
def check():
    global data
    data = Users.query.all()
    for d in data:
        print(d.email,d.password)
    return render_template('check.html',data=data)
@app.route('/display', methods=['GET', 'POST'])
def display():
    user = db.session.query(Users).filter(Users.email=="mail@mail.com").all()
    return render_template('display.html',data=user)
def field(lst,fields):
    global f,i,j,k,d2
    data=[]
    f=[len(x) for x in fields]
    for i in range(len(lst)):
        d=[]
        for j in range(len(lst[i])):
            for k in range(f[j]):
                d.append(getattr(lst[i][j],fields[j][k]))
            #d2=[getattr(lst[i][j],fields[j][k]) for k in range(f[j])]
        data.append(d)
    return data
def calc_age(data):
    days=[data[i][1].birthday for i in range(len(data))]
    days=[make_age(date) for date in days]
    return days
def calcAge(data,n):
    global s,ss
    for s in data:
        ss=s[n]
        ss.age=make_age(ss.birthday)
    return data
@app.route('/history', methods=['GET', 'POST'])
def history():
    global user
    #user = db.session.query(Users, Spec, History).join(Users, Users.email == Spec.email,Users.email == History.email).all()
    '''
    datas = ses.query(Shohin, Shohin.shohin_no, Shohin.name, Zaiko.shop_no, Zaiko.suryo, Shop.shop_name
).join(Zaiko, Zaiko.shohin_no == Shohin.shohin_no
).join(Shop, Shop.shop_no == Zaiko.shop_no)
    '''
    user = db.session.query(Users.email,Spec.name,History.date,History.symptom).join(Spec, Users.email == Spec.email).join(History, Users.email == History.email).all()
    #data=db.session.query(Users, Spec).join(Users, Users.email == Spec.email).all()
    return render_template('history.html',data=user)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False, port=8080)

