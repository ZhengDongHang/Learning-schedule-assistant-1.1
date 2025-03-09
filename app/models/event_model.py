import pymysql
from config import db_config

def insert_event(name, info, start_time, end_time, user):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS event (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                info TEXT,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                user VARCHAR(50) NOT NULL,
                FOREIGN KEY (user) REFERENCES users(account_number)
            )
            """
            cursor.execute(create_table_query)

            insert_query = """
            INSERT INTO event (name, info, start_time, end_time, user)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, info, start_time, end_time, user))
            connection.commit()
    finally:
        connection.close()