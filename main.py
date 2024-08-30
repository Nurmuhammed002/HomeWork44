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
#
# from aiogram import Bot, Dispatcher, executor
# import Homework3.fsm_store
# from config import TOKEN
# from Homework3 import fsm_store
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)
#
# Homework3.fsm_store.register_handlers(dp)
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)



import aioschedule
import asyncio
from aiogram import executor
from config import dp, bot
from Homework4.handlers.handlers import start_command, info_command, show_product, next_product
from Homework4.db_main import get_products

async def send_daily_updates():
    products = get_products()
    if not products:
        return

    product_list = "\n\n".join([f"ID: {p[1]}, Категория: {p[2]}, Информация: {p[3]}" for p in products])
    await bot.send_message(chat_id="YOUR_ADMIN_ID", text=f"Ежедневные обновления:\n\n{product_list}")

async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_updates)
    aioschedule.every().day.at("19:00").do(send_daily_updates)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

def start_scheduler(loop):
    asyncio.ensure_future(scheduler(), loop=loop)

def register_handlers(dp):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(info_command, commands="info")
    dp.register_message_handler(show_product, commands="show_products")
    dp.register_callback_query_handler(next_product, lambda c: c.data == 'next_product')

if __name__ == "__main__":
    register_handlers(dp)
    loop = asyncio.get_event_loop()
    start_scheduler(loop)
    executor.start_polling(dp, skip_updates=True, loop=loop)

import asyncio
from aiogram import executor
from config import dp
from Homework5.handlers  import register_handlers
import aioschedule
from Homework5.db_main import create_tables
from config import bot



async def send_daily_updates():
    products = get_products()
    if not products:
        return

    product_list = "\n\n".join([f"ID: {p[1]}, Категория: {p[2]}, Информация: {p[3]}" for p in products])
    await bot.send_message(chat_id="YOUR_ADMIN_ID", text=f"Ежедневные обновления:\n\n{product_list}")


async def scheduler():
    aioschedule.every().day.at("09:00").do(send_daily_updates)
    aioschedule.every().day.at("19:00").do(send_daily_updates)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def start_scheduler(loop):
    asyncio.ensure_future(scheduler(), loop=loop)



create_tables()


register_handlers(dp)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    start_scheduler(loop)

    executor.start_polling(dp, skip_updates=True)
