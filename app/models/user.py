import pymysql

def insert_user(name, account_number, password, db_config):
    db_config = db_config
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                account_number VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
            """
            cursor.execute(create_table_query)

            check_query = """
            SELECT COUNT(*) FROM users WHERE account_number = %s
            """
            cursor.execute(check_query, (account_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                return f"该账号已被占用，请换个账户: {account_number}"

            insert_query = """
            INSERT INTO users (name, account_number, password)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (name, account_number, password))
            connection.commit()
            return f"User with account_number: {account_number} has been added."
    finally:
        connection.close()

def check_user_credentials(account_number, password, db_config):
    db_config = db_config
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT account_number, name FROM users
            WHERE account_number = %s AND password = %s
            """
            cursor.execute(query, (account_number, password))
            result = cursor.fetchone()
            if result:
                return {'account_number': result[0], 'name': result[1]}
            else:
                return None
    finally:
        connection.close()
