from aiogram import types
from aiogram.dispatcher import FSMContext
from db_main import insert_collection
from FSM_online_store import ProductFSM
from buttons import get_main_menu_buttons


async def collection_start(message: types.Message):
    await ProductFSM.collection.set()
    await message.reply("Enter the collection for the product.", reply_markup=get_main_menu_buttons())


async def process_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        productid = data['productid']
        collection = message.text
        insert_collection(productid, collection)

    await message.reply("Collection added successfully.", reply_markup=get_main_menu_buttons())
    await state.finish()


def register_handlers(dp):
    dp.register_message_handler(collection_start, commands="add_collection")
    dp.register_message_handler(process_collection, state=ProductFSM.collection)
