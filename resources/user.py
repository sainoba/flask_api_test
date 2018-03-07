import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True,
        help="This field can't be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True,
        help="This field can't be left blank!"
    )

    def post(self):
        data = self.parser.parse_args()
        response = {"message": "User already exists"}, 400
        if UserModel.find_by_username(data["username"]) is None:
            user = UserModel(**data)
            user.save_to_db()
            response = {"message": "User created succesfully"}, 201
        return response
