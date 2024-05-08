from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Symptom
from .extensions import db
import datetime

data_blueprint = Blueprint('data_blueprint', __name__, template_folder='templates', static_folder='static')

@data_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    lang = request.args.get('lang', 'ja')
    if lang == 'en':
        return render_template('index_en.html')
    else:
        return render_template('index.html')

@data_blueprint.route('/notice', methods=['GET', 'POST'])


def notice():
    if request.method == 'POST':
        return redirect(url_for('data.symptom'))
    return render_template('notice.html')

@data_blueprint.route('/symptom', methods=['GET', 'POST'])
#@login_required
def symptom():
    if request.method == 'POST':
        user = Symptom(
            user_id=current_user.id,
            sex=request.form.get('sex', ''),
            birth_year=int(request.form.get('birth_year', 0)),
            birth_month=int(request.form.get('birth_month', 0)),
            birth_day=int(request.form.get('birth_day', 0)),
            onset_year=int(request.form.get('onset_year', 0)),
            onset_month=int(request.form.get('onset_month', 0)),
            onset_day=int(request.form.get('onset_day', 0)),
            morning_stiffness=request.form.get('morning_stiffness', ''),
            stiffness_duration=int(request.form.get('stiffness_duration', 0)),
            pain_level=int(request.form.get('pain_level', 0))       
        )
        
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました！', 'success')
        return redirect(url_for('data.joints_fig'))

    years = range(1920, datetime.date.today().year + 1)
    months = range(1, 13)
    days = range(1, 32)
    stiffness_durations = [0, 5, 10, 15, 20, 30, 40, 50, 60, 120]

    return render_template('symptom.html', years=years, months=months, days=days, stiffness_durations=stiffness_durations)

@data_blueprint.route('/joints_fig', methods=['GET', 'POST'])
#@login_required
def joints_fig():
    if request.method == 'POST':
        # フォームからのデータを処理する
        return redirect(url_for('data.labo_exam'))
    return render_template('joints_fig.html')

@data_blueprint.route('/labo_exam', methods=['GET', 'POST'])
#@login_required
def labo_exam():
    if request.method == 'POST':
        # フォームからのデータを処理する
        return redirect(url_for('data.handpicture'))
    return render_template('labo_exam.html')   

@data_blueprint.route('/handpicture', methods=['GET', 'POST'])
#@login_required
def handpicture():
    if request.method == 'POST':
        # アップロードされたファイルを処理する
        return redirect(url_for('data.x_ray'))
    return render_template('handpicture.html')

@data_blueprint.route('/x_ray', methods=['GET', 'POST'])
#@login_required
def x_ray():
    if request.method == 'POST':
        # アップロードされたファイルを処理する
        return redirect(url_for('data.drresult'))
    return render_template('x_ray.html')

@data_blueprint.route('/drresult', methods=['GET', 'POST'])
#@login_required
def result():
    user_id = current_user.id
    symptoms = Symptom.query.filter_by(user_id=user_id).first()
    # 結果を表示する
    return render_template('drresult.html', symptoms=symptoms)