from flask import Blueprint, render_template
from flask_restful import Resource, Api


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


class PingUsers(Resource):

    def get(self):
        return {
            "status": "success",
            "message": "pong"
        }


api.add_resource(PingUsers, '/users/ping')
