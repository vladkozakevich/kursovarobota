import requests
import time
from cachetools import TTLCache
from create import card_data

# Створюємо кеш з TTL (часом життя) 120 секундами для всіх функцій
api_cache = TTLCache(maxsize=200, ttl=120)


# Функція для отримання виписок з рахунку
async def get_statement_list(user_id, account_id, from_time, to_time=None):
    cache_key = f"statement_{account_id}_{from_time}_{to_time}"
    token_card, id_user = card_data.get_user_card_data(user_id)


    if cache_key in api_cache:
        timestamp, data = api_cache[cache_key]
        if time.time() - timestamp < 120:
            return data

    url = f"https://api.monobank.ua/personal/statement/{account_id}/{from_time}"
    if to_time:
        url += f"/{to_time}"

    headers = {
        "X-Token": f"{token_card}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        statement_data = response.json()
        api_cache[cache_key] = (time.time(), statement_data)
        return statement_data
    else:
        print("Error:", response.status_code)
        return None


# Функція для отримання даних користувача з картки
async def get_data_from_card_user(user_id):
    if user_id in api_cache:
        timestamp, data = api_cache[user_id]
        if time.time() - timestamp < 120:
            return data

    url = 'https://api.monobank.ua/personal/client-info'
    token_card, id_user = card_data.get_user_card_data(user_id)

    headers = {
        'X-Token': f'{token_card}',
    }

    response = requests.get(url, headers=headers)
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


# Функція для перевірки коду
async def check_code(user_id):
    token_card, id_user = card_data.get_user_card_data(user_id)

    url = 'https://api.monobank.ua/personal/client-info'
    headers = {
        'X-Token': f'{token_card}',
    }

    response = requests.get(url, headers=headers)

    return response


# Функція для отримання курсу обміну валют
async def get_exchange_rate(currency_code, data_acc):
    cache_key = f"exchange_rate_{currency_code}_{data_acc}"

    if cache_key in api_cache:
        timestamp, data = api_cache[cache_key]
        if time.time() - timestamp < 120:
            return data

    url = f"https://api.exchangerate-api.com/v4/latest/{data_acc}"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data["rates"][currency_code]

    api_cache[cache_key] = (time.time(), exchange_rate)
    return exchange_rate
