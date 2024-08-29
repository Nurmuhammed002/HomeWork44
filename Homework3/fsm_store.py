import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Homework3.buttons import get_sizes_keyboard  # Импортируем функцию для получения клавиатуры
from config import TOKEN  # Импортируйте ваш токен из конфигурационного файла

# Инициализация логирования, бота и диспетчера
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# Подключение к базе данных SQLite
def db_connect():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS products (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            name TEXT NOT NULL,  
            size TEXT NOT NULL,  
            category TEXT NOT NULL,  
            price REAL NOT NULL,  
            photo TEXT NOT NULL  
        )  
    ''')
    conn.commit()
    return conn


# Вставка данных в таблицу
def insert_product(data):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''  
        INSERT INTO products (name, size, category, price, photo)  
        VALUES (?, ?, ?, ?, ?)  
    ''', (data['name'], data['size'], data['category'], data['price'], data['photo']))
    conn.commit()
    conn.close()


# Определение состояний
class Store(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    confirmation = State()


# Начало диалога
@dp.message_handler(commands=["fsm_store"])
async def start(message: types.Message):
    await message.answer('What is the name of the product?')
    await Store.name.set()


# Обработка имени товара
@dp.message_handler(state=Store.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Size of the product?', reply_markup=get_sizes_keyboard())
    await Store.size.set()


# Обработка размера товара
@dp.message_handler(state=Store.size)
async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Category of the product?')
    await Store.category.set()


# Обработка категории товара
@dp.message_handler(state=Store.category)
async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Price of the product?')
    await Store.price.set()


# Обработка цены товара
@dp.message_handler(state=Store.price)
async def load_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Please enter a valid price (numbers only).')
        return
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Please send a photo of the product.')
    await Store.photo.set()


# Обработка фото товара
@dp.message_handler(state=Store.photo, content_types=['photo'])
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        confirmation_message = (
            f"Product Name: {data['name']}\n"
            f"Size: {data['size']}\n"
            f"Category: {data['category']}\n"
            f"Price: {data['price']}\n"
        )
        await message.answer_photo(
            photo=data['photo'],
            caption=confirmation_message
        )

        await message.answer("Are the details correct?", reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True).add(types.KeyboardButton("Yes"), types.KeyboardButton("No")))
        await Store.confirmation.set()

    # Подтверждение данных


@dp.message_handler(state=Store.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == "yes":
        async with state.proxy() as data:
            insert_product(data)  # Сохранение данных в базу
        await message.answer("Saved to database!")
        await state.finish()
    elif message.text.lower() == "no":
        await message.answer("Operation cancelled.")
        await state.finish()

    # Обработчик для команды отмены


@dp.message_handler(commands=["cancel"], state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Operation cancelled. Use /fsm_store to start over.")


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["fsm_store"])
    dp.register_message_handler(load_name, state=Store.name)
    dp.register_message_handler(load_size, state=Store.size)
    dp.register_message_handler(load_category, state=Store.category)
    dp.register_message_handler(load_price, state=Store.price)
    dp.register_message_handler(load_photo, state=Store.photo, content_types=['photo'])
    dp.register_message_handler(confirmation, state=Store.confirmation)
    dp.register_message_handler(cancel, commands=["cancel"], state='*')


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)