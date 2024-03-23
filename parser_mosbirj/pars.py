import requests
from bs4 import BeautifulSoup
from sql_function import databasework
import asyncio
from config import bot
import json
from itertools import groupby
import aiohttp
import datetime
import re
from get_html import get_html_page

def extract_version_number(s):
    # Функция для извлечения версионного номера из строки
    match = re.search(r'(\d+\.\d+)', s)
    if match:
        return float(match.group(1))
    return None

class mosbirja_parser:
    async def get_headers():
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        return headers
    
    
    
    async def start_mosbirja_parser():
        futures = await mosbirja_parser.pars_futures()
        print(futures)
        futures_stock = await mosbirja_parser.check_futures_stock(futures)
        
        
        with open("assets/data_futures_assets.json", "w") as json_file:
            json.dump(futures_stock, json_file, indent=4)
        await get_html_page(typee='futures_assets')
        
        futures_futures = await mosbirja_parser.check_futures_futures(futures)
        

        

        with open("assets/data_futures_futures.json", "w") as json_file:
            json.dump(futures_futures, json_file, indent=4)
        await get_html_page(typee='futures_futures')
            

            
        
    

    
    
    async def check_futures_stock(futures): # сортиуем и чекаем спред и годовую доходность фьючей и их акций
        futures_stock_list = []
        futures_data = await mosbirja_parser.get_stock_future()
        for list_future in futures:
            for future in list_future:
                flag = False
                
                for item in futures_data:  # забираем название акции
                    if item[1] == future:
                        stock = item[5]
                        print(stock)
                        code_future = item[0]
                        flag = True
                        break
                
            
                if flag == False:
                    continue
                
                
                
                price_stock = await mosbirja_parser.get_price_stock(stock)
                last_trade_date, lot_volume, settle_price = await mosbirja_parser.get_inf_future(code_future)
                
                print('------------------')
                print(f'Фьючерс - {future, code_future}')
                print(f'Акция - {stock}')
                print(f'Цена акции - {price_stock}')
                print(f'Последний день обращения - {last_trade_date}')
                print(f'Лотность - {lot_volume}')
                print(f'Цена фьючерса - {settle_price}')
                
                
                
                try:
                    
                    days_left = await mosbirja_parser.get_day_for_futures(last_trade_date)
                    if days_left <= 0:
                        continue
                    
                    spred_stock = ((settle_price/(price_stock*lot_volume)) -1)*100
                    year_dohod = (spred_stock/days_left)*365
                    
                    dict_future = {
                        "future_name": f'{future} ({settle_price}р)',
                        "stock": f'{stock} ({price_stock}р)',
                        "spred_stock": spred_stock,
                        "year_dohod": year_dohod
                        }
                    
                    if year_dohod > 25: # если годовая доходность больше 25%
                        price_stock = round(price_stock, 2)
                        typee = 'futures/assets'
                        await mosbirja_parser.send_msg(futures_data, future, stock, spred_stock, year_dohod, settle_price, price_stock, typee) # отправляем уведомление 
                    
                    
                    futures_stock_list.append(dict_future)
                except Exception as ex:
                    print(ex)
        
                
        
                
        return futures_stock_list
                
                
    async def check_futures_futures(futures): # берем фьючи и сортируем
        futures_futures_list = []
        futures_data = await mosbirja_parser.get_stock_future()
        
        for list_future in futures:
            # Преобразование строк в словарь {версионный_номер: строка}
            print(list_future)
            versions = {extract_version_number(s): s for s in list_future}

            # Сортировка версионных номеров по убыванию
            sorted_versions = sorted(versions.keys(), reverse=True)

            # Сравнение более старших с более ранними фьючерсами
            for i in range(len(futures)):
                for j in range(i+1, len(list_future)):
                    month_i, year_i = map(int, list_future[i].split('-')[1].split('.'))
                    month_j, year_j = map(int, list_future[j].split('-')[1].split('.'))
                    
                    if year_i < year_j or (year_i == year_j and month_i < month_j):
                        #print(f"{list_future[j]} с {list_future[i]}")
                        future_future = await mosbirja_parser.get_spred_futures_futures(list_future[j], list_future[i], futures_data)
                    else:
                        #print(f"{list_future[i]} с {list_future[j]}")
                        future_future = await mosbirja_parser.get_spred_futures_futures(list_future[i], list_future[j], futures_data)
                    if future_future:
                        futures_futures_list.append(future_future)
                
        
                
        return futures_futures_list       
                    
                    
            
                    
    async def get_spred_futures_futures(future1, future2, futures_data): # берем сперд и годовую доходность фьючей с фьючами
        # Формула по фьючерсам 
        # A - ближний фьючерс
        # B - дальний фьючерс 
        # A1 - количество дней до экспирации ближнего фьючерса
        # В1 - количество дней до экспирации дальнего фьючерса 
        # C - спред
        # D - годовая доходность

        # C = (B/A - 1)*100%
        #D= 365*C/(B1-A1) 


        #count = 0
        flag = False
        flag2 = False
        for item in futures_data:  # забираем код фьючерса
            if item[1] == future1:
                code_future1 = item[0]
                flag = True
        for item in futures_data:
            if item[1] == future2:
                code_future2 = item[0]
                flag2 = True
                
        if flag == False or flag2 == False:
            return
            
            
        last_trade_date1, lot_volume1, settle_price1 = await mosbirja_parser.get_inf_future(code_future1)
        last_trade_date2, lot_volume2, settle_price2 = await mosbirja_parser.get_inf_future(code_future2)
        
        

        
        
        days_left1 = await mosbirja_parser.get_day_for_futures(last_trade_date1)
        days_left2 = await mosbirja_parser.get_day_for_futures(last_trade_date2)
        if days_left1 < 0 or days_left2 < 0:
            return
        
        
        
        A = settle_price2
        B = settle_price1
        A1 = days_left2
        B1 = days_left1
        
        
        
        C = (B/A - 1)*100
        D = 365*C/(B1-A1) 
        
        dict_future = {
            "future_name": f'{future1} ({settle_price1}р)',
            "future2_name": f'{future2} ({settle_price2}р)',
            "spred_futures": C,
            "year_dohod": D
            }
        
        if D > 25: # если годовая доходность больше 25%
            typee = 'futures/futures'
            await mosbirja_parser.send_msg(futures_data, future1, future2, C, D, settle_price1, settle_price2, typee) # отправляем уведомление 
        
        
        # print('------------------')
        # print(f'Фьючерс - {future1, future2}')
        # print(f'spred_futures - {C}')
        # print(f'year_dohod - {D}')
        
        return dict_future


    async def get_day_for_futures(last_trade_date): # сколько дней до экспирации
        last_trade_date_splited = last_trade_date.split('-')
        
        future_date = datetime.datetime(int(last_trade_date_splited[0]), int(last_trade_date_splited[1]), int(last_trade_date_splited[2])).date()
        current_date = datetime.datetime.now().date()
        
        days_left = (future_date - current_date).days
        return int(days_left)
  
    async def get_stock_future(): # берем все фьючи чтоб достать из них базовую акцию
        link = 'https://iss.moex.com/iss/statistics/engines/futures/markets/forts/series.json'
        headers = await mosbirja_parser.get_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=link) as response:
                resp = await response.text()
        
        jsonresp = json.loads(resp)
        return jsonresp["series"]["data"]
                    
                
    
    
    
    async def pars_futures(): # парсер фьючей
        grouped_data = {}
        tasks = []
        futures = []
        for i in range(1, 11): # запускаем таски
            task = asyncio.create_task(mosbirja_parser.get_futures(i))
            await asyncio.sleep(0.4)
            tasks.append(task)
            
        # Ожидание завершения каждой задачи и получение результата
        for task in tasks:
            result = await task
            futures.extend(result)
                
            
        for item in futures: # разбиваем фьючи на списки
            key = item.split('-')[0]
            if key in grouped_data:
                grouped_data[key].append(item)
            else:
                grouped_data[key] = [item]

        # Преобразуем словарь в список списков
        result = list(grouped_data.values())
        return result # возвращаем список
            
            
    async def get_futures(i): # запрос
        
        futures = []
        link = f'https://www.moex.com/ru/derivatives/lastdata.aspx?pge={i}&gr=2&tp=F&sby=1'
        
        headers = await mosbirja_parser.get_headers()
        #resp = requests.get(url=link, headers=headers).text
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=link) as response:
                resp = await response.text()
        print(response.status)

        soup = BeautifulSoup(resp, "html.parser")
        
        table_scroller = soup.find('div', class_='table-scroller')
        if table_scroller:
            target_elements = table_scroller.find_all('tr', class_=['tr1', 'tr0'], attrs={'align': 'right'})
            for element in target_elements:
                link_element = element.find('a')
                if link_element:
                    #print(link_element.text)
                    futures.append(link_element.text)
                    
        return futures
        
        
        
    async def get_price_stock(stock): # получаем стоимость акции из апи
        try: 
            link = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{stock}.jsonp?iss.meta=off&iss.json=extended&callback=JSON_CALLBACK&lang=ru&iss.only=marketdata,securities'    
            headers = await mosbirja_parser.get_headers()
            
            async with aiohttp.ClientSession(headers=headers) as session: # запрос
                async with session.get(url=link) as response:
                    resp = await response.text()
            json_data = resp.replace('JSON_CALLBACK(', '').replace(')', '') # удаляем лишнее с ответа
            
            jsonresp = json.loads(json_data)
            last_value = jsonresp[1]["marketdata"][0]["LAST"] # забираем последнюю цену
            
            
            return float(last_value)
                
                
        except Exception as ex:
            print(ex)
            
            
    async def get_name_stock(stock): # получаем наименование акции из апи
        try: 
            link = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{stock}.jsonp?iss.meta=off&iss.json=extended&callback=JSON_CALLBACK&lang=ru&iss.only=marketdata,securities'    
            headers = await mosbirja_parser.get_headers()
            
            async with aiohttp.ClientSession(headers=headers) as session: # запрос
                async with session.get(url=link) as response:
                    resp = await response.text()
            json_data = resp.replace('JSON_CALLBACK(', '').replace(')', '') # удаляем лишнее с ответа
            
            jsonresp = json.loads(json_data)
            shortname = jsonresp[1]["securities"][0]["SHORTNAME"] # забираем последнюю цену
            
            
            return shortname
                
                
        except Exception as ex:
            print(ex)
            
    async def get_inf_future(code_future): # получаем всю нужную инфу о фьючерсе
        try: 
            link = f'https://iss.moex.com/iss/engines/futures/markets/forts/securities/{code_future}.jsonp?iss.meta=off&iss.json=extended&callback=JSON_CALLBACK&lang=ru&contractname=1'  
            headers = await mosbirja_parser.get_headers()
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url=link) as response:
                    resp = await response.text()
            json_data = resp.replace('JSON_CALLBACK(', '').replace(')', '') # удаляем лишнее с ответа
            jsonresp = json.loads(json_data)
            
            
            last_trade_date = jsonresp[1]["securities"][0]["LASTTRADEDATE"]
            lot_volume = jsonresp[1]["securities"][0]["LOTVOLUME"]
            settle_price = jsonresp[1]["marketdata"][0]["SETTLEPRICE"]
                    
            
            return (last_trade_date, lot_volume, settle_price)
                
                
        except Exception as ex:
            print(ex)
            
            
    
    async def send_msg(futures_data, future1, future2, spred, year_dohod, settle_price1, settle_price2, typee):
        try:
            
            find = await databasework.find_futures_in_db(future1, future2)
            if find == None:
                for item in futures_data:  # забираем код фьючерса
                    if item[1] == future1:
                        assets = item[5]
                        break
                 
                shortname = await mosbirja_parser.get_name_stock(assets) # берем название акции
                
                text = f'<b>({shortname})</b> {future1}({settle_price1}р) / {future2}({settle_price2}р) - {round(spred, 2)}% (годовая доходность {round(year_dohod, 2)}%)' # текст
                await databasework.insert_futures(future1, future2) # добавляем в бд
                
                if typee == 'futures/futures':
                
                    users = await databasework.get_all_user_with_sub_futures() # берем всех юзеров с подпиской на фьючерсы/фьючерсы
                elif typee == 'futures/assets':
                    users = await databasework.get_all_user_with_sub_assets() # берем всех юзеров с подпиской на фьючерсы/акции
                    
                    
                for user in users:
                    try:
                        await bot.send_message(chat_id=user[1], text=text, parse_mode='html')
                        await asyncio.sleep(0.4)
                    except: pass
                
        except Exception as ex:
            print(ex)
