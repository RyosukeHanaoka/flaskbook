from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Symptom, JointData
from .extensions import db
import datetime
import os
from .models import HandData
from PIL import Image

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
        data=request.form
        joint_entry = JointData(
            dip_joint_left_2=int(data.get('dip_joint_left_2', 0)),
            dip_joint_left_3=int(data.get('dip_joint_left_3', 0)),
            dip_joint_left_4=int(data.get('dip_joint_left_4', 0)),
            dip_joint_left_5=int(data.get('dip_joint_left_5', 0)),
            dip_joint_right_2=int(data.get('dip_joint_right_2', 0)),
            dip_joint_right_3=int(data.get('dip_joint_right_3', 0)),
            dip_joint_right_4=int(data.get('dip_joint_right_4', 0)),
            dip_joint_right_5=int(data.get('dip_joint_right_5', 0)),
            thumb_ip_joint_left=int(data.get('thumb_ip_joint_left', 0)),
            thumb_ip_joint_right=int(data.get('thumb_ip_joint_right', 0)),
            pip_joint_left_2=int(data.get('pip_joint_left_2', 0)),
            pip_joint_left_3=int(data.get('pip_joint_left_3', 0)),
            pip_joint_left_4=int(data.get('pip_joint_left_4', 0)),
            pip_joint_left_5=int(data.get('pip_joint_left_5', 0)),
            pip_joint_right_2=int(data.get('pip_joint_right_2', 0)),
            pip_joint_right_3=int(data.get('pip_joint_right_3', 0)),
            pip_joint_right_4=int(data.get('pip_joint_right_4', 0)),
            pip_joint_right_5=int(data.get('pip_joint_right_5', 0)),
            mp_joint_left_1=int(data.get('mp_joint_left_1', 0)),
            mp_joint_left_2=int(data.get('mp_joint_left_2', 0)),
            mp_joint_left_3=int(data.get('mp_joint_left_3', 0)),
            mp_joint_left_4=int(data.get('mp_joint_left_4', 0)),
            mp_joint_left_5=int(data.get('mp_joint_left_5', 0)),
            mp_joint_right_1=int(data.get('mp_joint_right_1', 0)),
            mp_joint_right_2=int(data.get('mp_joint_right_2', 0)),
            mp_joint_right_3=int(data.get('mp_joint_right_3', 0)),
            mp_joint_right_4=int(data.get('mp_joint_right_4', 0)),
            mp_joint_right_5=int(data.get('mp_joint_right_5', 0)),
            wrist_joint_hand_left=int(data.get('wrist_joint_hand_left', 0)),
            wrist_joint_hand_right=int(data.get('wrist_joint_hand_right', 0)),
            elbow_joint_left=int(data.get('elbow_joint_left', 0)),
            elbow_joint_right=int(data.get('elbow_joint_right', 0)),
            shoulder_joint_left=int(data.get('shoulder_joint_left', 0)),
            shoulder_joint_right=int(data.get('shoulder_joint_right', 0)),
            hip_joint_left=int(data.get('hip_joint_left', 0)),
            hip_joint_right=int(data.get('hip_joint_right', 0)),
            knee_joint_left=int(data.get('knee_joint_left', 0)),
            knee_joint_right=int(data.get('knee_joint_right', 0)),
            ankle_joint_left=int(data.get('ankle_joint_left', 0)),
            ankle_joint_right=int(data.get('ankle_joint_right', 0)),
            mtp_joint_left_1=int(data.get('mtp_joint_left_1', 0)),
            mtp_joint_left_2=int(data.get('mtp_joint_left_2', 0)),
            mtp_joint_left_3=int(data.get('mtp_joint_left_3', 0)),
            mtp_joint_left_4=int(data.get('mtp_joint_left_4', 0)),
            mtp_joint_left_5=int(data.get('mtp_joint_left_5', 0)),
            mtp_joint_right_1=int(data.get('mtp_joint_right_1', 0)),
            mtp_joint_right_2=int(data.get('mtp_joint_right_2', 0)),
            mtp_joint_right_3=int(data.get('mtp_joint_right_3', 0)),
            mtp_joint_right_4=int(data.get('mtp_joint_right_4', 0)),
            mtp_joint_right_5=int(data.get('mtp_joint_right_5', 0)),
            distal_joints=int(data.get('distal_joints', 0)),
            proximal_joints=int(data.get('proximal_joints', 0))
        )
        db.session.add(joint_entry)
        db.session.commit()

        return redirect(url_for('data_blueprint.labo_exam'))
    return render_template('joints_fig.html')

        # distal_joints と proximal_joints の計算と保存
def distal_joints(joint_entry):
    distal_joints = sum(
        [getattr(joint_entry, f"pip_joint_left_{i}", 0) for i in range(2, 6)] + \
        [getattr(joint_entry, f"pip_joint_right_{i}", 0) for i in range(2, 6)]+ \
        [getattr(joint_entry, f"mtp_joint_left_{i}", 0) for i in range(1, 6)]+ \
        [getattr(joint_entry, f"mtp_joint_right_{i}", 0) for i in range(1, 6)]+ \
        getattr(joint_entry, "thumb_ip_joint_left", 0) + \
        getattr(joint_entry, "thumb_ip_joint_right", 0)+ \
        getattr(joint_entry, "hand_wrist_joint_left", 0) + \
        getattr(joint_entry, "hand_wrist_joint_right", 0))
    return distal_joints

def proximal_joints(joint_entry):
    proximal_joints = sum(
        getattr(joint_entry, f"elbow_joint_left", 0), 
        getattr(joint_entry, f"shoulder_joint_left", 0),
        getattr(joint_entry, f"elbow_joint_right", 0),
        getattr(joint_entry, f"shoulder_joint_right", 0),
        getattr(joint_entry, f"hip_joint_left", 0),
        getattr(joint_entry, f"hip_joint_right", 0),
        getattr(joint_entry, f"knee_joint_left", 0),
        getattr(joint_entry, f"knee_joint_right", 0),
        getattr(joint_entry, f"ankle_joint_left", 0),
        getattr(joint_entry, f"ankle_joint_right", 0)
    )
    return proximal_joints    

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
    if request.method == 'POST':# アップロードされたファイルを処理する
        # 右手の写真をアップロードから取得
        right_hand = request.files['right_hand']
        # 左手の写真をアップロードから取得
        left_hand = request.files['left_hand']

        # 現在の日時を取得
        now = datetime.now()
        # 日時をファイル名に使用する形式に変換
        dt_string = now.strftime("%Y%m%d_%H%M%S")

        # 右手の写真のファイル名を変更
        right_filename = f"{current_user.email}_{dt_string}_right.jpg"
        # 右手の写真を保存するパス
        right_path = os.path.join("apps/data/rt_hand", right_filename)
        # 右手の写真を保存
        right_hand.save(right_path)

        # 左手の写真を左右反転
        left_img = Image.open(left_hand)
        left_img_flipped = left_img.transpose(Image.FLIP_LEFT_RIGHT)

        # 左手の写真のファイル名を変更
        left_filename = f"{current_user.email}_{dt_string}_left.jpg"
        # 左手の写真を保存するパス
        left_path = os.path.join("apps/data/lt_hand", left_filename)
        # 左手の写真を保存
        left_img_flipped.save(left_path)

        # データベースに保存
        hand_data = HandData(
            user_id=current_user.id,
            datetime=now,
            right_hand_path=right_path,
            left_hand_path=left_path
        )
        db.session.add(hand_data)
        db.session.commit()

        return redirect(url_for('data.x_ray'))

    return render_template('handpicture.html')        
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