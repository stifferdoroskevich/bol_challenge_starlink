import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    try:
        connection = psycopg2.connect(
            database=os.getenv("DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST", "127.0.0.1"),
            port=os.getenv("PORT", "5432")
        )
        return connection
    except Exception as e:
        print(e.args)


def create_schema():
    connection = connect_to_db()
    connection.autocommit = True
    cursor = connection.cursor()
    sql = '''CREATE SCHEMA IF NOT EXISTS blue'''
    cursor.execute(sql)


def create_tables():
    connection = connect_to_db()
    connection.autocommit = True
    cursor = connection.cursor()
    sql = """CREATE TABLE IF NOT EXISTS blue.starlink_ts
                (id varchar NOT NULL, 
                creation_date timestamp NOT NULL, 
                longitude float NOT NULL, 
                latitude float NOT NULL
                )
        """
    try:
        with connection:
            cursor.execute(sql)
            print("Table created successfully")
    except Exception as e:
        print(e.args)


if __name__ == '__main__':
    create_schema()
    create_tables()
