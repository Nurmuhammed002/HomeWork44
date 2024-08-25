import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Кнопки для клавиатуры
start_button = KeyboardButton('/start')
quiz_button = KeyboardButton('/quiz')
game_button = KeyboardButton('/game')
game_duel_button = KeyboardButton('/game_duel')
end_button = KeyboardButton('/end')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(start_button, quiz_button, game_button, game_duel_button, end_button)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Выберите команду для начала:", reply_markup=keyboard)

@dp.message_handler(commands=['end'])
async def end_command(message: types.Message):
    await message.answer("Завершение работы бота. До свидания!")

@dp.message_handler(commands=['quiz'])
async def send_quiz(message: types.Message):
    question = "What is the capital of France?"
    options = ["Berlin", "Paris", "Rome", "Madrid"]
    correct_option = 1
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        type='quiz',
        correct_option_id=correct_option,
        is_anonymous=False
    )

@dp.message_handler(commands=['game'])
async def game_dice(message: types.Message):
    games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
    chosen_game = random.choice(games)
    await bot.send_dice(message.chat.id, emoji=chosen_game)

@dp.message_handler(commands=['game_duel'])
async def game_duel(message: types.Message):
    games = ['⚽', '🎯', '🎲']
    bot_game = random.choice(games)
    player_game = random.choice(games)

    bot_dice = await bot.send_dice(message.chat.id, emoji=bot_game)
    player_dice = await bot.send_dice(message.chat.id, emoji=player_game)

    if bot_dice.dice.value > player_dice.dice.value:
        await message.answer("Бот выиграл!")
    elif bot_dice.dice.value < player_dice.dice.value:
        await message.answer("Вы выиграли!")
    else:
        await message.answer("Ничья!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
