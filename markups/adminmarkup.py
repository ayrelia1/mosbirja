from config import types, InlineKeyboardBuilder
import filters.filtersbot as filtersbot
from sql_function import databasework
import asyncio


def admin_markup():
    markup = (
        InlineKeyboardBuilder()

        .button(text='✉️ Рассылка', callback_data='mailing')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


def main_admin():
    markup = (
        InlineKeyboardBuilder()
        .button(text='🔙 В меню', callback_data='main_admin')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


