from sqlalchemy.sql import func
from project import db, bcrypt, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    full_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    admin = db.Column(db.Boolean(), default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'admin': self.admin,
            'created_date': self.created_date,
        }

    def __init__(self, full_name, username, email, password, admin=False):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()
        self.admin = admin

    def __repr__(self):
        return f"{self.full_name}, {self.email}, {self.username}"

    def is_admin(self):
        return self.admin

    def is_authenticated(self):
        return True


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))
