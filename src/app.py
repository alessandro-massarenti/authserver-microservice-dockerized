#!/usr/bin/python3

import config

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
import jwt
import datetime

from werkzeug.security import check_password_hash

from dbh import Dbh

import json

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = config.SECRET_KEY

db = Dbh()


# Resources classes-----------------------------------------------------------------------------------------------------

class Login(Resource):
    # Path responsable for giving out jwt to people who are logged in
    def get(self):
        self.login()

    def sign_token(data: dict) -> str:
        prova = {'user': 'username'}

        payload: dict = {
            'iss': 'apiserver',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }

        payload.update(prova)

        token = jwt.encode(
            payload,
            app.config['SECRET_KEY'], algorithm="HS512")

        return token


class Users(Resource):
    @staticmethod
    def get():
        utenti = db.select('SELECT * FROM users.accounts')

        return utenti, 200


class UsersId(Resource):

    @staticmethod
    def get(email: str):
        utenti = db.select('SELECT * FROM users.accounts WHERE email = %s', (email,))

        return utenti, 200

    def post(self):
        # Create new user
        # Requires json payload with:
        # name, surname, email, password

        pass

    def put(self):
        pass


# Resource adding to the API -------------------------------------------------------------------------------------------

api.add_resource(Users, '/users')
api.add_resource(UsersId, '/users/<string:email>')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
