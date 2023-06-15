import psycopg2
import hashlib
from config import host, user, password, db_name, port

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")

    with connection.cursor() as cursor:
        cursor.execute(
            f'''INSERT INTO users (username, email, password_hash)
                VALUES ('VovaK13', 'acdefg@mail.ru', %s)
            ''',
            (str(hashlib.md5(b'12345').hexdigest()), )
        )
        cursor.execute(
            f'''INSERT INTO users (username, email, password_hash)
                        VALUES ('Octopus', 'octopus@mail.ru', %s)
                    ''', (str(hashlib.md5(b'qwerty').hexdigest()), )
        )
        print('Users added!')
except Exception as ex:
    print('Error while working with PostgreSQL!', ex)
finally:
    if connection:
        connection.close()
        print('PostgreSQL connection is closed!')
