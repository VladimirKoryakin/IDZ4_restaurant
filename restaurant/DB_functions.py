import psycopg2
from SQL_queries import *
from config import host, user, password, db_name, port, Config

connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
connection.autocommit = True


def get_user_info_by_id(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_USER_INFO_BY_ID, (user_id,))
            res = cursor.fetchone()
    return res


def delete_expired_tokens():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_EXPIRED_TOKENS)


def delete_previous_tokens(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_OLD_TOKENS_BY_USER_ID, (user_id,))


def get_user_info_by_email(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ID_BY_EMAIL, (email,))
            user_id = cursor.fetchone()[0]
            cursor.execute(SELECT_PASSWORD_HASH_BY_ID, (user_id,))
            password_hash = cursor.fetchone()[0]
    return [user_id, password_hash]


def is_the_username_taken(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_USERS_WITH_THE_SAME_USERNAME, (username,))
            num = cursor.fetchone()[0]
    if num > 0:
        return True
    return False


def is_the_email_taken(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_USERS_WITH_THE_SAME_EMAIL, (email,))
            num = cursor.fetchone()[0]
    if num > 0:
        return True
    return False


def is_role_correct(role):
    if role in {'chef', 'customer', 'manager'}:
        return True
    else:
        return False


def get_user_id_by_token(token):
    user_id = False
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_USER_ID_BY_TOKEN, (token,))
            res = cursor.fetchone()
            if res:
                user_id = res[0]
    return user_id

