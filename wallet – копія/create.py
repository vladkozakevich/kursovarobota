from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database.bd import History, Card

from config import TOKEN

history = History()      # створення екземлпяру класа з історією

card_data = Card('wallet')       # створення екземлпяру класа з даними карти

storage = MemoryStorage()  # створення фсм


bot = Bot(TOKEN)  # створення екзмепляру бота
dp = Dispatcher(bot=bot,storage=storage)  # створення обробника
