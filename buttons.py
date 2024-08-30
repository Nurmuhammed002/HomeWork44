from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/start"))
    keyboard.add(KeyboardButton("/info"))
    keyboard.add(KeyboardButton("/show_products"))  # Кнопка для показа продуктов
    return keyboard

def get_product_buttons():
    keyboard = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton("Далее", callback_data='next_product')
    keyboard.add(next_button)
    return keyboard
