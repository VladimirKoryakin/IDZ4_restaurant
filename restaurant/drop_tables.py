import psycopg2
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
        cursor.execute(
            "DROP TABLE sessions;"
        )
        cursor.execute(
            "DROP TABLE users;"
        )
        print("Tables deleted!")
except Exception as ex:
    print('Error while working with PostgreSQL!', ex)
finally:
    if connection:
        connection.close()
        print('PostgreSQL connection is closed!')
