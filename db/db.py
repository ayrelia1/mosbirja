import psycopg2
import os

def connect():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_LOG"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    return connection
