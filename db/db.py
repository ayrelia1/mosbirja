import psycopg2
from config import file_config



def connect():
    connection = psycopg2.connect(
        host=file_config['db_host'],
        user=file_config['db_log'],
        password=file_config['db_pass'],
        database=file_config['db_name']
    )
    return connection
