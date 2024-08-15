from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await message.answer(str(int(message.text) ** 2))
    else:
        await message.answer(message.text)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

@dp.message_handler(commands=['sendfile'])
async def send_file(message: types.Message):
    with open("path/to/your/file.txt", "rb") as file:
        await message.answer_document(file)
