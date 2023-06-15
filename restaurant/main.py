from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import psycopg2
import hashlib
from config import host, user, password, db_name, port, Config
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from SQL_queries import *
from DB_functions import *

connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
connection.autocommit = True

app = Flask(__name__)
app.config.from_object(Config)
api = Api()

jwt = JWTManager(app)


def get_jwt(user_id, expire_time=24):
    token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(expire_time)
    )
    return token


def authorize_user(email, user_password):
    user_id = get_user_info_by_email(email)[0]
    password_hash = get_user_info_by_email(email)[1]
    if password_hash == hashlib.md5(user_password.encode()).hexdigest():
        return user_id
    else:
        return -1


class Registration(Resource):
    def post(self):
        try:
            data = request.get_json()
        except Exception as ex:
            return "Request should be in JSON format!", 406

        try:
            username = data['username']
            email = data['email']
            password = data['password']
        except Exception as ex:
            return "Incorrect input format, there should be username, email and password in JSON!", 400
        role = ''
        if 'role' in data:
            role = data['role']

        if '@' not in email:
            return "Incorrect email address!", 400
        if is_the_username_taken(username):
            return "The username is already taken, try another one.", 400
        if is_the_email_taken(email):
            return "The user with the same email address already exists, try another one.", 400
        if role != '' and not is_role_correct(role):
            return "The role of the user is invalid!", 400

        try:
            with connection:
                with connection.cursor() as cursor:
                    if role != '':
                        cursor.execute(INSERT_USER_WITH_ROLE_RETURN_ID,
                                       (username, email, hashlib.md5(password.encode()).hexdigest(), role,))
                    else:
                        cursor.execute(INSERT_USER_RETURN_ID,
                                       (username, email, hashlib.md5(password.encode()).hexdigest(),))
                    user_id = cursor.fetchone()[0]
            return {"id": user_id, "message": f"User {username} is succesfully created!"}, 201
        except Exception as ex:
            print(ex)
            return "Something went wrong with the database!", 500


class Authorization(Resource):
    def post(self):
        try:
            data = request.get_json()
        except Exception as ex:
            return "Request should be in JSON format!", 406

        try:
            email = data['email']
            password = data['password']
        except Exception as ex:
            return "Incorrect input format, there should be email and password in JSON!", 400

        if not is_the_email_taken(email):
            return "There is no user with such email, try to register first.", 400

        user_id = authorize_user(email, password)
        if user_id < 0:
            return "The password is incorrect!", 400

        delete_expired_tokens()
        delete_previous_tokens(user_id)
        token = get_jwt(user_id)
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(INSERT_SESSION, (user_id, token,))
            return f"User {user_id} is successfully authorised with token: {token}", 200
        except Exception as ex:
            print(ex)
            return "Something went wrong with the database!", 500


class UserInfo(Resource):
    def get(self):
        try:
            data = request.get_json()
        except Exception as ex:
            return "Request should be in JSON format!", 406

        try:
            token = data['token']
        except Exception as ex:
            return "Incorrect input format, there should be a token in JSON!", 400

        delete_expired_tokens()
        user_id = get_user_id_by_token(token)
        if not user_id:
            return "Invalid token, try to reauthorize.", 400

        info = get_user_info_by_id(user_id)

        return "User info ---  " + f"user_id: {user_id}     username: {info[0]}    " \
            f" email: {info[1]}     role: {info[2]}      created_at: {info[3]}       updated_at: {info[4]}", 200


api.add_resource(Registration, "/api/registration")
api.add_resource(Authorization, "/api/authorization")
api.add_resource(UserInfo, "/api/user_info")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")

