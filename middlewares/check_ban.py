from config import *
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject
from sql_function import databasework
import datetime

class BannedMiddleware(BaseMiddleware): # ---- > мидлвар чек на бан
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        check_user = await databasework.check_user(event.from_user.id) # ---> достаем юзера
        if check_user == None: # если юзера нет - 
            await databasework.create_user(event) # - создаем юзера
            return await handler(event, data)
        
        check_ban = await databasework.check_ban(event.from_user.id) # проверяем на бан
        if check_ban == 'yes':
            return await bot.send_message(event.from_user.id, (f'Banned!'))

        return await handler(event, data)