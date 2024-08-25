import logging
from config import dp
from aiogram.utils import executor
from handlers import echo, quiz, start
from db import database
from Lesson import bot

async def on_startup(_):
    await database.sql_create()

def start_bot():
    echo.register_echo(dp)
    quiz.register_quiz(dp)
    start.register_start(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_bot()
