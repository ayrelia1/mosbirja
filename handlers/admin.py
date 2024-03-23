from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, file_config, json, FSInputFile, time
from markups.adminmarkup import *
import filters.filtersbot as filtersbot
from sql_function import databasework
from datetime import timedelta
from markups.markup import menu
import datetime
import filters.filtersbot as filtersbot
import aiocron
import random
import asyncio
from states.adminstates import MailingState
import threading
import os
import requests
import re
import logging
    
router = Router()

router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру


# назад в админ меню
@router.callback_query(F.data == 'main_admin')
async def admin_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    markup = admin_markup()
    count_users = await databasework.get_count_users()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'💎 Вы попали в админ-панель\n\n⚙️ Количество пользователей в боте - {count_users}', reply_markup=markup)


# админка
@router.message(F.text == '/admin')
async def start(message: types.Message, state: FSMContext):
    #photo = FSInputFile('kwork8/photo/start_message.jpg')
    await state.clear()
    markup = admin_markup()
    count_users = await databasework.get_count_users()
    await message.answer(f'💎 Вы попали в админ-панель\n\n⚙️ Количество пользователей в боте - {count_users}', reply_markup=markup)
    
    
# рассылка
@router.callback_query(F.data == 'mailing')
async def mailing(callback: types.CallbackQuery, state: FSMContext):
    markup = main_admin()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'💎 Отправьте сообщение для рассылки', reply_markup=markup)
    await state.set_state(MailingState.one)
    
# рассылаем
@router.message(MailingState.one)
async def send_msg_mailing(message: types.Message, state: FSMContext):
    users = await databasework.get_all_status_user()
    
    success = 0
    error = 0
    
    for user in users:
        try:
            await bot.copy_message(from_chat_id=message.chat.id, chat_id=user[1], message_id=message.message_id)
            await asyncio.sleep(0.2)
            success += 1
        except:
            error += 1
            
            
    markup = main_admin()
    await message.answer(f'💎 Рассылка успешно завершена!\n\nОтправленных сообщений - {success}\nОшибок - {error}', reply_markup=markup)
    await state.clear()
    
admin = router
