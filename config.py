from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile, InputFile
from aiogram.types import FSInputFile
from aiogram.types import (
    KeyboardButton,
    Message,
    Update,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
import time
import asyncio
from aiogram import types
from aiogram.filters import Filter
import logging
import datetime
import json
from dotenv import load_dotenv
import os



load_dotenv()

current_folder = os.path.dirname(os.path.abspath(__file__))

with open(f'{current_folder}/config_bot.json', 'r+') as file:
    file_config = json.load(file)
     




dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="html")




