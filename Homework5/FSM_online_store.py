from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from db_main import insert_collection
from buttons import get_main_menu_buttons


class ProductFSM(StatesGroup):
    name = State()
    category = State()
    sizes = State()
    price = State()
    article = State()
    photo = State()
    collection = State()


async def process_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text
        productid = data['productid']
        collection = data['collection']

        insert_collection(productid, collection)

    await message.reply("Продукт добавлен в коллекцию!", reply_markup=get_main_menu_buttons())
    await state.finish()
