from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_sizes_keyboard():
    sizes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    sizes = ["XL", "3XL", "M", "S", "L"]
    sizes_keyboard.add(*[KeyboardButton(size) for size in sizes])
    return sizes_keyboard