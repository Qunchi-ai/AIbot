import os
from dotenv import load_dotenv

# Загружаем переменные из .env (локально)
load_dotenv()

# Читаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Превращаем ADMIN_ID в число, если возможно
try:
    ADMIN_ID = int(ADMIN_ID)
except (TypeError, ValueError):
    ADMIN_ID = None

# Проверки
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден. Добавьте его в .env или переменные Railway.")

if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID не найден. Добавьте его в .env или переменные Railway.")
