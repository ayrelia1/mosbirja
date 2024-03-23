from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, file_config, json, FSInputFile, time, InputFile
from markups.markup import *
import filters.filtersbot as filtersbot
from sql_function import databasework
from datetime import timedelta
import datetime
import filters.filtersbot as filtersbot
import random
import asyncio
import threading
import os
import requests
import re
from get_html import get_html_page
router = Router()






# хендлер старта
@router.message(F.text == '/start')
async def start(message: types.Message, state: FSMContext):
    #photo = FSInputFile('kwork8/photo/start_message.jpg')
    await state.clear()
    markup = await start_markup(message.from_user.id)
    await message.answer(f'💎 Добро пожаловать в бота по расчету спредов на МосБирже!\n\n⚙️ Подпишитесь на уведмления от бота, бот будет вам присылать сигналы!', reply_markup=markup)
    



# вкл/выкл подписки
@router.callback_query(F.data == 'enable_disable_sub_assets')
async def enable_disable_sub_assets_handler(callback: types.CallbackQuery):
    user = await databasework.check_user(callback.from_user.id) 
    
    await databasework.enable_disable_sub_db_assets(callback.from_user.id)
    markup = await start_markup(callback.from_user.id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
    
# вкл/выкл подписки на фьючерсы
@router.callback_query(F.data == 'enable_disable_sub_futures')
async def enable_disable_sub_futures_handler(callback: types.CallbackQuery):
    user = await databasework.check_user(callback.from_user.id) 
    
    await databasework.enable_disable_sub_db_futures(callback.from_user.id)
    markup = await start_markup(callback.from_user.id)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)


@router.callback_query(F.data == 'get_report_futures_assets')
async def future_assets(callback: types.CallbackQuery):
    
    #typee='futures_assets'
    #file = await get_html_page(typee)
    
    document = FSInputFile('mosbirja/assets/output_futures_assets.html', filename='report.html')

    await bot.send_document(chat_id=callback.message.chat.id, caption='⚙️ Отчет фьючерсы/акции', document=document)


@router.callback_query(F.data == 'get_report_futures_futures')
async def futures_futures(callback: types.CallbackQuery):
    
    #typee='futures_futures'
    #file = await get_html_page(typee)
    
    document = FSInputFile('mosbirja/assets/output_futures_futures.html', filename='report.html')

    await bot.send_document(chat_id=callback.message.chat.id, caption='⚙️ Отчет фьючерсы/фьючерсы', document=document)
user = router