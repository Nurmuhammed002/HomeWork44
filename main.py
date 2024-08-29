# import logging
#
# import Homework3.FSM_online_store
# from config import dp
# from aiogram.utils import executor
# # from handlers import echo, quiz, start
# from db import database
# from Homework2 import bot
#
# async def on_startup(_):
#     await database.sql_create()
#
#
# # echo.register_echo(dp)
# # quiz.register_quiz(dp)
# # start.register_start(dp)
# Homework3.FSM_online_store.register_FSM_online_store(dp=dp)
# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher, executor
import Homework3.fsm_store
from config import TOKEN
from Homework3 import fsm_store

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

Homework3.fsm_store.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




