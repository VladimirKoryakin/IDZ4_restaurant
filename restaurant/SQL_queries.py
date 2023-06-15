INSERT_USER_RETURN_ID = '''INSERT INTO users (username, email, password_hash) 
                            VALUES (%s, %s, %s) RETURNING id'''

INSERT_USER_WITH_ROLE_RETURN_ID = '''INSERT INTO users (username, email, password_hash, role) 
                            VALUES (%s, %s, %s, %s) RETURNING id;'''

COUNT_USERS_WITH_THE_SAME_USERNAME = '''SELECT COUNT(*) FROM users WHERE username = %s;'''

COUNT_USERS_WITH_THE_SAME_EMAIL = '''SELECT COUNT(*) FROM users WHERE email = %s;'''

SELECT_ID_BY_EMAIL = '''SELECT id FROM users WHERE email = %s;'''

SELECT_PASSWORD_HASH_BY_ID = '''SELECT password_hash FROM users WHERE id = %s;'''

INSERT_SESSION = '''INSERT INTO sessions (user_id, session_token, expires_at) 
                            VALUES (%s, %s, CURRENT_TIMESTAMP(3) + interval '1 day');'''

DELETE_EXPIRED_TOKENS = '''DELETE FROM sessions WHERE CURRENT_TIMESTAMP(3) > expires_at;'''

SELECT_ACTIVE_SESSION_BY_USER_ID = '''SELECT session_token FROM sessions WHERE user_id = %s;'''

DELETE_OLD_TOKENS_BY_USER_ID = '''DELETE FROM sessions WHERE user_id = %s;'''

SELECT_USER_ID_BY_TOKEN = '''SELECT user_id FROM sessions WHERE session_token = %s;'''

SELECT_USER_INFO_BY_ID = '''SELECT username, email, role, created_at, updated_at FROM users WHERE id = %s;'''
