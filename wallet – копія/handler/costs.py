import os
import time

from datetime import datetime, timedelta
from cachetools import TTLCache

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from create import history, card_data
from keyboard import keyboard
from create import bot
from mono import get_statement_list

api_cache = TTLCache(maxsize=500, ttl=120)


class FSM(StatesGroup):
    # реєстрація всм машини стану
    bal = State()
    new_bal = State()


async def costs_main(callback: types.CallbackQuery):
    # обробка inline клавіатури
    if callback.data == 'costs_history':
        account_id = "0"
        current_time = int(time.time())
        thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())
        statement_list = await get_statement_list(callback.from_user.id, account_id, thirty_days_ago, current_time)

        user_id = callback.from_user.id
        history_file = history.create_history_file_from_card(user_id, statement_list)
        if history_file:
            with open(history_file, 'rb') as file:
                await callback.message.delete()
                await bot.send_document(chat_id=user_id, document=file)
                await callback.message.answer("<i>⬆️ в файлі вище зібрана вся історія ваших витрачень</i>",
                                              reply_markup=keyboard.all_logg(), parse_mode='HTML')
                os.remove(history_file)
        else:
            await callback.message.edit_text(
                "<i>Ви ще нічого не витратили ‼️\nЗробіть витрату щоб відкрити можливість переглядати меню</i>",
                reply_markup=keyboard.costs_back(), parse_mode='HTML')

    elif callback.data == 'costs_back':
        message_delete = callback.message.message_id - 1
        message_delete_2 = callback.message.message_id
        await bot.delete_message(callback.message.chat.id, message_delete)
        await bot.delete_message(callback.message.chat.id, message_delete_2)
        await callback.message.answer(
            "<i>📊 В цьому розділі ви можете відстежувати та формувати статистику на основі здійснених витрат</i>",
            reply_markup=keyboard.costs_menu(top_up_available=True), parse_mode='HTML')


def register_cost(dp: Dispatcher):
    # реєстрація хендлерів
    dp.register_callback_query_handler(costs_main, lambda callback_query: callback_query.data.startswith('costs'))
