from datetime import datetime, timedelta
import io
import time

import text
import matplotlib.pyplot as plt

from aiogram import types

from create import history, bot, card_data
from mono import get_statement_list, get_data_from_card_user
from create import Dispatcher
from keyboard import keyboard


async def statistic_m(callback: types.CallbackQuery):
    current_time = int(time.time())
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

    dat = await get_statement_list(callback.from_user.id, '0', thirty_days_ago, current_time)
    res = []

    subtract_history = history.get_add_history_by_id_from_card(dat)
    print(subtract_history)

    for i in subtract_history:
        res.append(i['amount'])
    print(res)
    average = sum(res) / len(res)
    print(average)

    amounts = [entry['amount'] for entry in subtract_history]
    dates = [str(entry['timestamp']) for entry in subtract_history]

    formatted_dates = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]
    x_labels = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(formatted_dates)), amounts)
    plt.xlabel('Дата')
    plt.ylabel('Сума')
    plt.title('Графік витрат')

    for i, amount in enumerate(amounts):
        plt.text(i, amount + 0.1, str(amount), ha='center')

    if len(amounts) <= 10:
        step = 2
    elif 10 < len(amounts) <= 30:
        step = 3
    elif 30 < len(amounts) <= 60:
        step = 5
    elif 60 < len(amounts) <= 90:
        step = 5
    elif 90 < len(amounts) <= 120:
        step = 5
    else:
        step = 10

    name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)

    plt.xticks(range(0, len(formatted_dates), step), [date for i, date in enumerate(x_labels) if i % step == 0])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    total = accounts
    de = average
    print(total, de)
    await callback.message.edit_text("<b>Нижче ви можете ознайомитись зі статистикою</b>", parse_mode='HTML')
    await callback.message.answer_photo(photo=types.InputFile(buf, filename='graph.png'))
    await callback.message.answer(
        '<b>📊 коротко про ваші витрати ⬇️</b>\n\n'
        f'<i>Всього витрачено</i> <b>{round(sum(res), 2)} '
        f'{data_acc}</b>\n\n'
        f'<i>Максимум ви витратили</i> '
        f'<b>{max(res)}</b>',
        reply_markup=keyboard.stat_back(),
        parse_mode='HTML'
    )

    buf.close()


async def statistic_a(callback: types.CallbackQuery):
    current_time = int(time.time())
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

    dat = await get_statement_list(callback.from_user.id, '0', thirty_days_ago, current_time)

    subtract_history = history.get_m_history_by_id_from_card(dat)
    print(subtract_history)
    res = []
    for i in subtract_history:
        res.append(i['amount'])

    average = sum(res) / len(res)

    amounts = [entry['amount'] for entry in subtract_history]
    dates = [str(entry['timestamp']) for entry in subtract_history]

    formatted_dates = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]
    x_labels = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(formatted_dates)), amounts)
    plt.xlabel('Дата')
    plt.ylabel('Сума')
    plt.title('Графік поповнень')

    for i, amount in enumerate(amounts):
        plt.text(i, amount + 0.1, str(amount), ha='center')

    if len(amounts) <= 10:
        step = 2
    elif 10 < len(amounts) <= 30:
        step = 3
    elif 30 < len(amounts) <= 60:
        step = 5
    elif 60 < len(amounts) <= 90:
        step = 5
    elif 90 < len(amounts) <= 120:
        step = 5
    else:
        step = 10

    name, accounts, data_acc, card_n = await get_data_from_card_user(callback.from_user.id)


    plt.xticks(range(0, len(formatted_dates), step), [date for i, date in enumerate(x_labels) if i % step == 0])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    await callback.message.edit_text("<b>Нижче ви можете ознайомитись зі статистикою</b>", parse_mode='HTML')
    await callback.message.answer_photo(photo=types.InputFile(buf, filename='graph.png'))
    await callback.message.answer('<b>📊 коротко про ваші поповнення ⬇️</b>\n\n'
                                  f'<i>Взагалом ви поповнили</i> <b>{sum(res)}'
                                  f' {data_acc}</b>\n\n'
                                  f'<i>Максимум ви поповнили свій баланс на {max(res)}</i>',
                                  reply_markup=keyboard.stat_back(), parse_mode='HTML')

    buf.close()


async def stats(calback: types.CallbackQuery):
    if calback.data == 'statistick_back':
        message_1 = calback.message.message_id - 2
        message_2 = calback.message.message_id - 1
        message_3 = calback.message.message_id
        await bot.delete_message(calback.message.chat.id, message_1)
        await bot.delete_message(calback.message.chat.id, message_2)
        await bot.delete_message(calback.message.chat.id, message_3)
        await calback.message.answer(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")
    elif calback.data == 'statistick_back_main':
        await calback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")


def register_cost(dp: Dispatcher):
    dp.register_callback_query_handler(statistic_m, text='statistick_minuse')
    dp.register_callback_query_handler(statistic_a, text='statistick_add')
    dp.register_callback_query_handler(stats, text=['statistick_back', 'statistick_back_main'])
