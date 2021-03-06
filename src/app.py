#!/usr/bin/python3

import config

from flask import Flask
from flask_restful import Api, Resource, reqparse
import jwt
import datetime
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
from usermodel import UserModel

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = config.SECRET_KEY


def sign_token(data: dict = {}) -> str:
    payload: dict = {
        'iss': config.SERVER_NAME,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    payload.update(data)

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'], algorithm="HS512")

    return token


# Resources classes-----------------------------------------------------------------------------------------------------
Login_get_args = reqparse.RequestParser()
Login_get_args.add_argument("name")


class Login(Resource):

    # Path responsable for giving out jwt to people who are logged in
    @staticmethod
    def get():
        data = request.get_json()

        # Richiede i dati di login, ovvero nome utente e password
        if not data['email'] and not data['password']:
            return {"Error": "Bad request"}, 400

        user = UserModel(data['email'])

        # confronta i dati inseriti con quelli presenti nel database
        if not check_password_hash(user.password, data['password']):
            return {"Error": "Unauthorized"}, 401

        # ritorna un token jwt con le info prescelte
        return {"token": sign_token()}, 200

    @staticmethod
    def post():
        data = request.get_json()

        if not data['email'] and not data['password'] and not data['name'] and not data['surname']:
            return {"Error": "Bad request"}, 400

        data['password'] = generate_password_hash(data['password'])

        user = UserModel(data['email'])
        user.name = data['name']
        user.surname = data['surname']
        user.password = data['password']

        try:
            user.push()
        except KeyError:
            return {"Error": "Server error"}, 500
        except FileExistsError:
            return {"Error": "Email already in the database"}, 400

        return {"Msg": "inserito utente"}, 200


# class RUsers(Resource, DbIface):
#
#   @staticmethod
#    def get():
#
#
#        return utenti, 200
#
#    def post(self):
#        # Create new user
#        # Requires json payload with:
#       # name, surname, email, password
#       pass


# class RUsersById(Resource):
#
#    @staticmethod
#    def get(email: str):
#        utenti = db.select('SELECT * FROM users.accounts WHERE email = %s', (email,))
#
#       return utenti, 200
#
#    def put(self):
#        pass


# Resource adding to the API -------------------------------------------------------------------------------------------

# api.add_resource(RUsers, '/users')
# api.add_resource(RUsersById, '/users/<string:email>')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
