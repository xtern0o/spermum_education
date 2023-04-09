# 1db2c74
from flask import Flask, render_template, redirect, flash, get_flashed_messages, url_for, abort, jsonify, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from data import db_session
from data.users import Users
from data.groups import Groups
from data.messages import Messages
from data.questions import Questions

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.chat_form import ChatForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "maxkarnlol"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return "Index"


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(f"/profile/{user.id}")
            return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
        return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = Users(
            email=form.email.data,
            remember=form.remember.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
        )
        teacher_type = request.form.get("teacher-button")
        student_type = request.form.get("student-button")
        if student_type:
            user.user_type = "student"
        else:
            user.user_type = "teacher"
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember.data)
        return redirect("/profile")
    return render_template("register.html", title="Регистрация", form=form)


@app.route('/chat', methods=['POST', 'GET'])
@login_required
def chat():
    form = ChatForm()
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == 1).first()
    groups = user.groups
    if form.validate_on_submit():
        print(form.message.data)
    data = {
        'groups': groups,
        'first_group': groups[0]
    }
    return render_template('chat.html', title='Чат', form=form, **data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/spermum.db")
    app.run(host="127.0.0.1", port=5000)
