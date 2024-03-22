from config import types, InlineKeyboardBuilder
import filters.filtersbot as filtersbot
from sql_function import databasework
import asyncio


async def start_markup(user_id): # async чтоб запрос к бд сделать
    user = await databasework.check_user(user_id) # берем юзера
    
    text_assets = { # если вкл или выкл
        "off": "🔴 Подписаться акции",
        "on": "🟢 Отписаться акции"
    }
    text_futures = { # если вкл или выкл
        "off": "🔴 Подписаться фьючерсы",
        "on": "🟢 Отписаться фьючерсы"
    }
    
    markup = (
        InlineKeyboardBuilder()
        .button(text=f'{text_assets[user[4]]}', callback_data='enable_disable_sub_assets') # ставим из бд выключено или включено ⚙️
        .button(text=f'{text_futures[user[7]]}', callback_data='enable_disable_sub_futures') # ставим из бд выключено или включено ⚙️
        .button(text='⚙️ Фьючерсы/Акции', callback_data='get_report_futures_assets')
        .button(text='⚙️ Фьючерсы/Фьючерсы', callback_data='get_report_futures_futures')
        .adjust(2, 2, repeat=True)
        .as_markup()
    )
    
    return markup


def menu():
    markup = (
        InlineKeyboardBuilder()
        .button(text='🔙 В главное меню', callback_data='main')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


