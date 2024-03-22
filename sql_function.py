from config import types
from db.db import connect
import random
import string
import datetime
import requests
import json
import base64
import pandas as pd
from io import BytesIO

class databasework:
    
    
    
    async def enable_disable_sub_db_assets(user_id): # вкл/выкл подписки на акции
        connection = connect()
        user = await databasework.check_user(user_id) # берем юзера
        
        if user[4] == 'off': # если включен то выключаем
            par = 'on'
        elif user[4] == 'on': # если выключен то включаем
            par = 'off'
        
        with connection.cursor() as cursor:
            sql = "UPDATE users SET subscribe_assets = %s WHERE user_id = %s" # делаем запрос
            cursor.execute(sql, (par, str(user_id),))
            connection.commit()
        connection.close()

    async def enable_disable_sub_db_futures(user_id): # вкл/выкл подписки на фьючерсы
        connection = connect()
        user = await databasework.check_user(user_id) # берем юзера
        
        if user[7] == 'off': # если включен то выключаем
            par = 'on'
        elif user[7] == 'on': # если выключен то включаем
            par = 'off'
        
        with connection.cursor() as cursor:
            sql = "UPDATE users SET subscribe_futures = %s WHERE user_id = %s" # делаем запрос
            cursor.execute(sql, (par, str(user_id),))
            connection.commit()
        connection.close()
    
    
    
    async def create_user(message: types.Message): # создание юзера в бд
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM users WHERE user_id = %s") # проверка есть ли юзер
            cursor.execute(sql, (str(message.chat.id),))
            result = cursor.fetchone()
            if result == None:
                sql = ("INSERT INTO users (user_id, username) VALUES (%s, %s)") # если нет создаем
                cursor.execute(sql, (str(message.chat.id), str(message.from_user.username),))
                connection.commit()
        connection.close()
        
    async def check_user(id): # проверяем юзера в бд
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(sql, (str(id),))
            result = cursor.fetchone()
        connection.close()
        return result
                
                
                
    async def check_ban(tg_id): # проверяем юзера на бан в бд
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(sql, (str(tg_id),))
            result = cursor.fetchone()
            check_ban = result[5]
        connection.close()
        return check_ban    

    async def check_admin(message: types.Message): # проверяем админ ли юзер в бд
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(sql, (str(message.from_user.id),))
            result = cursor.fetchone()
            check_admin = result[3] 
        connection.close()
        return check_admin == 'admin'
    
    
    
    async def get_all_user(): # получаем всех юзеров
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    async def get_all_user_with_sub_assets(): # получаем всех юзеров с подпиской на фьючерсы/акции
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE subscribe_assets = 'on'"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    async def get_all_user_with_sub_futures(): # получаем всех юзеров с подпиской на фьючерсы/фьючерсы
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE subscribe_futures = 'on'"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    async def find_futures_in_db(future1, future2): # ищем было ли уведомление о годовом доходе уже
        connection = connect()
        date1 = datetime.datetime.now() - datetime.timedelta(hours=8)
        date2 = datetime.datetime.now()
        
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM year_dohod WHERE assets1 = %s AND assets2 = %s AND datetime BETWEEN %s AND %s"
            cursor.execute(sql, (future1, future2, date1, date2,))
            result = cursor.fetchone()
        connection.close()
        return result
    
    
    async def insert_futures(future1, future2): # если годовая доходность превысила 25% добавляем в бд
        connection = connect()
        date = datetime.datetime.now()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO year_dohod (assets1, assets2, datetime) VALUES (%s, %s, %s)") # если нет создаем
            cursor.execute(sql, (future1, future2, date,))
            connection.commit()
        connection.close()