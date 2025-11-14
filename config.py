import os
# from dotenv import load_dotenv # <--- УДАЛИТЕ ИЛИ ЗАКОММЕНТИРУЙТЕ ЭТО
#
# # Загружаем переменные из .env (локально)
# load_dotenv() # <--- УДАЛИТЕ ИЛИ ЗАКОММЕНТИРУЙТЕ ЭТО

# Читаем переменные окружения (теперь они берутся напрямую из окружения Railway)
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
    # Ваше сообщение об ошибке, которое вы видите
    raise ValueError("❌ ADMIN_ID не найден. Добавьте его в .env или переменные Railway.")