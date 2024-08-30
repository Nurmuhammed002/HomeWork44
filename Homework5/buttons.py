from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Start")
    info_button = KeyboardButton("Info")
    show_products_button = KeyboardButton("Show Products")
    add_collection_button = KeyboardButton("Add Collection")

    keyboard.add(start_button, info_button)
    keyboard.add(show_products_button, add_collection_button)

    return keyboard
