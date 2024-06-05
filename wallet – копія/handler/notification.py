import datetime

from create import card_data, bot


async def notification(data):
    # отримання вебхуків та подальше їх оброблення
    user_id_card = data['data']['account']
    amount = data['data']['statementItem']['amount'] / 100.0
    balance = data['data']['statementItem']['balance'] / 100.0
    webhook_time = data['data']['statementItem']['time']
    dt_object = datetime.datetime.fromtimestamp(webhook_time)
    who = data['data']['statementItem']['description']

    currency = 'UAH'


    formatted_time = dt_object.strftime("%H:%M")

    token_card = card_data.get_all_card_data()

    for row in token_card:
        user_id, db_user_id, token, status = row

        if token == user_id_card:
            if amount < 0:
                await bot.send_message(
                    chat_id=user_id,
                    text=(
                        f'✅ <b>Оплата була здійснена успішно.</b>\n'
                        f'💳 <i>Ви витратили</i> <b>{abs(amount)} {currency}</b> <i>в</i> <b>{formatted_time}</b>.\n'
                        f'👤 <i>Одержувач:</i> <b>{who}</b>\n'
                        f'💵 <i>Тепер ваш баланс нараховує</i> <b>{balance} {currency}</b>.'
                    ),
                    parse_mode='HTML'
                )

            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=(
                        f'✅ <b>Оплата була здійснена успішно.</b>\n'
                        f'💰 <i>Ви поповнили свою картку на</i> <b>{amount} {currency}</b> <i>в</i> <b>{formatted_time}</b>.\n'
                        f'👤 <i>Відправник:</i> <b>{who}</b>\n'
                        f'💵 <i>Тепер ваш баланс нараховує</i> <b>{balance} {currency}</b>.'
                    ),
                    parse_mode='HTML'
                )