from config import *

from .check_ban import BannedMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
def setup(dp: Dispatcher):


    banned_middleware = BannedMiddleware()
    dp.message.outer_middleware.register(banned_middleware)
    dp.callback_query.outer_middleware.register(banned_middleware)
    

    dp.callback_query.middleware(CallbackAnswerMiddleware())
    
    