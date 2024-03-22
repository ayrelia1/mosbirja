from config import dp, logging, asyncio, bot, file_config, Bot
from handlers import routers
from middlewares import setup
from aiogram.types import BotCommand, BotCommandScopeDefault
from db.models import create_database
from sql_function import databasework
from parser_mosbirj.pars import mosbirja_parser



@dp.startup()
async def start_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='🔄 Главное меню'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

            
            
            
async def start_parser():
    
    while True:
        print('start parser')
        try:
            await mosbirja_parser.start_mosbirja_parser()
        except Exception as ex:
            print(ex)
        
        await asyncio.sleep(file_config['time_pars'])
    
            

async def main() -> None:     # функция запуска бота
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s" 
                        ) # логирование
    
    
    for router in routers:
        dp.include_router(router) # импорт роутеров
    
    task1 = asyncio.create_task(create_database.create_users()) # создаем базу юзеров если нет
    task2 = asyncio.create_task(create_database.create_year_dohod()) # создаем базу в которой будут доходы
    
    
    task1 = asyncio.create_task(start_parser()) # создаем базу юзеров если нет
    
    
    setup(dp)  # мидлвари    
    await dp.start_polling(bot) # запуск поллинга
    
if __name__ == "__main__":
    asyncio.run(main()) 