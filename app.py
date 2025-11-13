import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import register_handlers
from db import init_db

logging.basicConfig(level=logging.INFO)

def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)

    # Добавляем хранение состояний — ЭТО ГЛАВНОЕ
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
