from db.db import connect
import asyncio

class create_database:
    
    
    
    
    async def create_users(): # ----------> создание таблицы users
        connection = connect()
        with connection.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS users (
                    ID SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    username VARCHAR(100) DEFAULT NULL,
                    status VARCHAR(25) CHECK (status IN ('user', 'admin')) DEFAULT 'user',
                    subscribe_assets VARCHAR(25) CHECK (subscribe IN ('on', 'off')) DEFAULT 'off',
                    subscribe_futures VARCHAR(25) CHECK (subscribe IN ('on', 'off')) DEFAULT 'off',
                    reg_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    ban VARCHAR(25) CHECK (ban IN ('yes', 'no')) DEFAULT 'no'
                    
                );"""
            cursor.execute(sql)
            connection.commit()
        connection.close()
        
        
        
    async def create_year_dohod(): # ----------> создание таблицы codes_oktmo
        connection = connect()
        with connection.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS year_dohod (
                    ID SERIAL PRIMARY KEY,
                    assets1 VARCHAR(255),
                    assets2 VARCHAR(255),
                    datetime TIMESTAMP
                );"""
            sql2 = 'CREATE INDEX ass1 ON year_dohod(assets1);'
            sql3 = 'CREATE INDEX ass2 ON year_dohod(assets2);'
            cursor.execute(sql)
            connection.commit()
            cursor.execute(sql2)
            connection.commit()
            cursor.execute(sql3)
            connection.commit()
        connection.close()
        
        
        
        
    

