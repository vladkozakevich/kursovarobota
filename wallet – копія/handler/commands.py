from aiogram import types, Dispatcher

from create import bot, card_data
from keyboard import keyboard


async def start(message: types.Message):
    # обробка команди /start
    token_card = card_data.get_all_card_data()
    for i in token_card:
        print(i)
    await message.answer(
        "<b>Привіт 👋🏼</b>\n\nЯ бот, створений для обліку твоїх фінансів та утворення статистики, "
        "щоб зробити управління грошима більш зручним. \n\n",
        reply_markup=keyboard.main_keyboard(), parse_mode='HTML')


def register_commands(dp: Dispatcher):
    # реєстрація хендлерів

    dp.register_message_handler(start, commands=['start', 'help'])
