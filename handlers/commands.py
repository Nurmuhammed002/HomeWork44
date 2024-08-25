from aiogram import types, Dispatcher
from config import bot
import os
from aiogram.types import InputFile
import random
from db import db_main


# @dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Привет!')
    await message.reply(text='Привет')

    await message.answer(text='Привет!')
    print(message.from_user.id)
    await db_main.sql_insert_registration(telegram_id=message.from_user.id,
                                          firstname=message.from_user.first_name)


async def info_handler(message: types.Message):
    await message.answer("Бот для группы 44-2 Backend")

    async def mem_handler(message: types.Message):
        path = 'media/'
        files = []

        for f in os.listdir(path):
            full_path = os.path.join(path, f)
            if os.path.isfile(full_path):
                files.append(full_path)

        random_photo = random.choice(files)

        await message.answer_photo(photo=InputFile(random_photo))

    def register_commands(dp: Dispatcher):
        dp.register_message_handler(start_handler, commands=['start'])
        dp.register_message_handler(info_handler, commands=['info'])
        dp.register_message_handler(mem_handler, text='отправь мем')