from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_restful import Resource, Api
from project.app.forms import RegistrationForm, LoginForm, EditProfileForm
from flask_login import logout_user, login_user, current_user, login_required
from project.app.models import User
from project import bcrypt, db
from werkzeug.urls import url_parse


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            if not current_user.is_admin():
                users_list = [user for user in User.query.all()]
                return redirect(url_for('.index', users=users_list))
            return redirect(url_for('.index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
                flash("Invalid Username or Password")
                return redirect(url_for('.login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('.index')
            return redirect(next_page)
        return render_template("login.html", title="Sign In", form=form)
    except Exception as e:
        return e


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


@users_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        db.session.commit()
        flash("You changes have been saved")
        return redirect(url_for('.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


class PingUsers(Resource):

    def get(self):
        return {
            "status": "success",
            "message": "pong"
        }


api.add_resource(PingUsers, '/users/ping')
