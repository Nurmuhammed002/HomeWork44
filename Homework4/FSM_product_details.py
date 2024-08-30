from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from Homework4.db_main import add_product


class ProductDetailsFSM(StatesGroup):
    productid = State()
    category = State()
    infoproduct = State()

async def start_product_details(message: types.Message):
    await ProductDetailsFSM.productid.set()
    await message.reply("Введите ID продукта:")

async def set_productid(message: types.Message, state: FSMContext):
    await state.update_data(productid=message.text)
    await ProductDetailsFSM.next()
    await message.reply("Введите категорию продукта:")

async def set_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await ProductDetailsFSM.next()
    await message.reply("Введите информацию о продукте:")

async def set_infoproduct(message: types.Message, state: FSMContext):
    data = await state.get_data()
    productid = data['productid']
    category = message.text
    infoproduct = data['infoproduct']

    add_product(productid, category, infoproduct)
    await state.finish()
    await message.reply("Информация о продукте сохранена!")

def register_handlers(dp):
    dp.register_message_handler(start_product_details, commands="add_product", state=None)
    dp.register_message_handler(set_productid, state=ProductDetailsFSM.productid)
    dp.register_message_handler(set_category, state=ProductDetailsFSM.category)
    dp.register_message_handler(set_infoproduct, state=ProductDetailsFSM.infoproduct)
