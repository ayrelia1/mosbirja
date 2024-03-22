from config import *
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject
from sql_function import databasework
import datetime

class CallbackMiddleware(BaseMiddleware): # ---- > мидлвар чек на бан
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        await bot.answer_callback_query(event.from_user.id)

        return await handler(event, data)