import asyncio

import requests

import text
import time
import re

from cachetools import TTLCache

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create import card_data
from keyboard import keyboard


from mono import check_code, get_exchange_rate, get_statement_list
from text import currency_data, currency_list, currency_data_trns, currency_get

api_cache = TTLCache(maxsize=100, ttl=120)


async def process_conversion(callback):
    # функція для конвератції балансу в інші валютм
    name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)
    global flag_base
    await callback.message.edit_text("<i>⏳ отримую актуальні данні, секунду...</i>", parse_mode='HTML')
    await asyncio.sleep(0.1)

    base_currency = currency_get.get(list(currency_get.values()).index(data_acc) + 1)
    print(base_currency)
    print(data_acc)
    euro_amount = accounts

    results = []
    for target_currency in currency_list:
        if target_currency == base_currency:
            continue

        exchange_rate = await get_exchange_rate(target_currency, data_acc)
        converted_amount = euro_amount * exchange_rate
        flag_base = currency_data.get(list(currency_get.keys())[list(currency_get.values()).index(base_currency)])
        flag_target = currency_data.get(list(currency_get.keys())[list(currency_get.values()).index(target_currency)])

        result_line = f'<b>{converted_amount:.2f}</b>  <i>{flag_target} ({currency_data_trns[target_currency]})</i>'
        results.append(result_line)

    unique_results = list(set(results))
    result_text = "\n".join(unique_results)
    await callback.message.edit_text(f'<i>💰 Ваш баланс</i> <b>{euro_amount:.2f} '
                                     f'{flag_base}</b>.\n\n<i>💱 Конвертація у інші валюти:</i>\n\n{result_text}',
                                     reply_markup=keyboard.back_conv(), parse_mode="HTML")


class FSM(StatesGroup):  # клас для фсм машини стану
    bal = State()
    welcome = State()
    pred = State()
    card = State()


async def get_data_from_card_user(user_id):
    # отрмання даних про користувача
    global api_cache

    if user_id in api_cache:
        timestamp, data = api_cache[user_id]
        if time.time() - timestamp < 60:
            return data

    response = await check_code(user_id)
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        accounts = data['accounts'][0]['balance'] / 100.0
        data_acc = data['accounts'][0]['cashbackType']
        card_n = data['accounts'][0]['maskedPan'][0]
        print(data['clientId'])

        api_cache[user_id] = (time.time(), (name, accounts, data_acc, card_n))

        return name, accounts, data_acc, card_n
    else:
        print("Помилка при запиті:", response.status_code)


async def money(callback: types.CallbackQuery):
    # обробка inline клавіатури
    if card_data.get_user_card(callback.from_user.id) == "Підключено":
        name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)
        if callback.data == "main_balance":
            if card_data.get_user_card(callback.from_user.id) != "Підключено":
                await callback.message.edit_text(
                    f"<i>💰 Ваш баланс складає</i> <b>{accounts} {data_acc}</b>",
                    reply_markup=keyboard.balance(top_up_available=True), parse_mode='HTML')
            else:
                await callback.message.edit_text(
                    f"<i>💰 Ваш баланс складає</i> <b>{accounts} {data_acc}</b>",
                    reply_markup=keyboard.balance(), parse_mode='HTML')

        elif callback.data == "main_costs":
            await callback.message.edit_text(
                "<i>📊 В цьому розділі ви можете відстежувати та формувати статистику на основі здійснених витрат</i>",
                reply_markup=keyboard.costs_menu(top_up_available=True), parse_mode='HTML')

        elif callback.data == 'main_static':
            await callback.message.edit_text(
                '<i>📊 В цьому розділі ви маєте можливість переглядати статистику щодо ваших поповнень та витрат</i>',
                reply_markup=keyboard.statistick(), parse_mode='HTML')
    else:
        await callback.answer('⁉️ Карта не підключена')
    if callback.data == 'main_card':
        try:
            if card_data.get_user_card(callback.from_user.id) == "Підключено":
                name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)
                mess = f"""
💳 Карта підключена.\n
🪪 Дані користувача:\n
👤 Користувач: {name}
💰 Рахунок: {accounts:.2f} {data_acc}
🛡 Номер карти: {card_n}"""

                await callback.message.edit_text(mess,
                                                 reply_markup=keyboard.back_in_main_card("🗑 Видалити карту", 'delete'))

            else:
                await callback.message.edit_text('⁉️ Карта не підключена', reply_markup=keyboard.card_menu())

        except Exception as ex:
            await callback.message.edit_text("⁉️ Ви ввели не вірний токен")


async def card(callback: types.CallbackQuery):
    # обробка inline клавіатури
    if callback.data == 'card_insert':
        await FSM.card.set()
        await callback.message.edit_text("📍 Введіть токен", reply_markup=keyboard.back())
    if callback.data == 'card_delete':
        card_data.delete_card(callback.from_user.id)
        await callback.message.edit_text('🗑 Карта успішно відключен', reply_markup=keyboard.card_menu())
    if callback.data == 'card_change':
        await FSM.card.set()
        await callback.message.edit_text("📍 Введіть новий токен", reply_markup=keyboard.back())


async def add_money(callback: types.CallbackQuery):
    # обробка inline клавіатури
    name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)
    if callback.data == 'add_konvert':
        await process_conversion(callback)
    elif callback.data == "add_back":
        await callback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")
    elif callback.data == 'add_back_b':
        await callback.message.edit_text(
            f"<i>💰 Ваш баланс складає</i> <b>{accounts} {data_acc}</b>",
            reply_markup=keyboard.balance(), parse_mode='HTML')


async def back_all_menu(callback: types.CallbackQuery):
    # обробка inline клавіатури
    if callback.data == 'back':
        await callback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")

    if callback.data == 'back_to_card':
        await callback.message.edit_text('⁉️ Карта не підключена', reply_markup=keyboard.card_menu())


async def card_insert(message: types.Message, state: FSMContext):
    # обробка токена який вводить користувач
    pattern = re.compile(r'^[a-zA-Z0-9-_]+$')

    if message.text and pattern.match(message.text):
        async with state.proxy() as data:
            url = 'https://api.monobank.ua/personal/client-info'
            headers = {
                'X-Token': f'{message.text}',
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                await message.answer(
                    f"<i>✅ Ваш токен прийнято</i> <b>{message.text}</b>",
                    reply_markup=keyboard.back_in_main_card("❌ Видалити карту", 'delete'), parse_mode='HTML')
                card_data.card_add(user_id=message.from_user.id, card=message.text, user_id_card=response.json()['accounts'][0]['id'], card_val='Підключено')
                await state.finish()
            else:
                await message.answer(
                    f"<i>❌ Ваш токен не прийнято</i> <b>{message.text}</b>",
                    reply_markup=keyboard.back_in_main_card('❕ Замінити токен', 'change'), parse_mode='HTML')
                card_data.card_add(user_id=message.from_user.id, card='message.text', user_id_card='id', card_val='Не підключено')
                await state.finish()

    else:
        await message.answer(
            f"<i>❌ Ваш токен не прийнято</i> <b>{message.text}</b>",
            reply_markup=keyboard.back_in_main_card('Замінити токен', 'change'), parse_mode='HTML')
        await state.finish()


async def back_with_fsm_rules(callback: types.CallbackQuery, state: FSMContext):
    # функція для завершення фсм машини стану
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(
        text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")


def register_balance(dp: Dispatcher):
    # реєстрація хендлерів
    dp.register_message_handler(get_exchange_rate, commands=['p'])
    dp.register_callback_query_handler(money, lambda callback_query: callback_query.data.startswith('main'))
    dp.register_callback_query_handler(card, lambda callback_query: callback_query.data.startswith('card'))
    dp.register_callback_query_handler(add_money, lambda callback_query: callback_query.data.startswith('add'))
    dp.register_callback_query_handler(back_all_menu, lambda callback_query: callback_query.data.startswith('back'))
    dp.register_message_handler(card_insert, state=FSM.card)
    dp.register_callback_query_handler(back_with_fsm_rules, state="*", text='fsm_back')
