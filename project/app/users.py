from flask import Blueprint, render_template, url_for, redirect, flash
from flask_restful import Resource, Api
from project.app.forms import RegistrationForm, LoginForm
from flask_login import logout_user, login_user, current_user
from project.app.models import User
from project import bcrypt, db


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for('.login'))
        login_user(user)
        return redirect(url_for('.index'))
    return render_template("login.html", title="Sign In", form=form)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(full_name=form.full_name.data, username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are Now a registered User")
        return redirect(url_for('.login'))
    return render_template('register.html', title="Register", form=form)


class PingUsers(Resource):

    def get(self):
        return {
            "status": "success",
            "message": "pong"
        }


api.add_resource(PingUsers, '/users/ping')
