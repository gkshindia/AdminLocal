from flask import Blueprint, render_template
from flask_restful import Resource, Api
from project.app.forms import Registration


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET'])
def index():
    form = Registration()
    return render_template('register.html', form=form)


class PingUsers(Resource):

    def get(self):
        return {
            "status": "success",
            "message": "pong"
        }


api.add_resource(PingUsers, '/users/ping')
