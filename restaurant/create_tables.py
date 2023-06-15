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

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(10) CHECK (role IN ('customer', 'chef', 'manager')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(3),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(3));
            '''
        )
        print('Table created!')

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE sessions (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                session_token VARCHAR(1000) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                );
            '''
        )
        print('Table created!')


except Exception as ex:
    print('Error while working with PostgreSQL!', ex)
finally:
    if connection:
        connection.close()
        print('PostgreSQL connection is closed!')
