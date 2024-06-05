import asyncio
import requests

from aiohttp import web

from create import dp
from handler import commands, statistic, costs, balance

from handler.notification import notification

webhook_registration_url = "https://api.monobank.ua/personal/webhook"

your_webhook_url = "https://a2ab-46-229-61-77.ngrok-free.app/webhook"

AUTH_TOKEN = "uCY6se42UdYbNXb4y3tgDwfwDXoNWI4aS4LzYdNhsj6o"

# Відправка запиту на реєстрацію вебхука
response = requests.post(
    webhook_registration_url,
    json={"webHookUrl": your_webhook_url},
    headers={"X-Token": AUTH_TOKEN}
)

# Перевірка статусу відповіді
if response.status_code == 200:
    print("Вебхук успішно зареєстровано!")
else:
    print("Помилка реєстрації вебхука:", response.text)


# Обробник вебхука
async def webhook_listener(request):
    if request.method == 'POST':
        try:
            data = await request.json()
            print(f"Отримано дані вебхука: {data}")
            await notification(data)
            return web.json_response({"status": "success"}, status=200)
        except Exception as e:
            print(f"Помилка обробки POST-запиту: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=500)
    elif request.method == 'GET':
        print("Отримано GET-запит для перевірки URL")
        return web.Response(status=200)


# Запуск сервера aiohttp
async def start_aiohttp_server():
    app = web.Application()
    app.router.add_post('/webhook', webhook_listener)
    app.router.add_get('/webhook', webhook_listener)  # Додано для обробки GET-запитів
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    print("Сервер запущено на порту 5000")
    while True:
        await asyncio.sleep(3600)


# Запуск Telegram бота
async def start_telegram_bot():
    statistic.register_cost(dp)
    balance.register_balance(dp)
    commands.register_commands(dp)
    costs.register_cost(dp)

    print('БОТ УСПІШНО ЗАПУСТИВСЯ')
    await dp.start_polling()


# Головна функція для запуску всіх процесів
async def main():
    # Створюємо задачі для серверу і бота
    aiohttp_task = asyncio.create_task(start_aiohttp_server())
    telegram_bot_task = asyncio.create_task(start_telegram_bot())

    # Чекаємо завершення всіх задач
    await asyncio.gather(aiohttp_task, telegram_bot_task)


if __name__ == '__main__':
    asyncio.run(main())
