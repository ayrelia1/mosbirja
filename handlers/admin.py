from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, file_config, json, bot_config_path, FSInputFile, time
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
import threading
import os
import requests
import re
import logging
    
router = Router()

router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру







@router.message(F.text == '/admin')
async def start(message: types.Message, state: FSMContext):
    #photo = FSInputFile('kwork8/photo/start_message.jpg')
    await state.clear()
    markup = admin_markup()
    await message.answer(f'💎 Вы попали в админ-панель', reply_markup=markup)
    
    
    
    
admin = router
