import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден. Добавьте его в переменные Railway.")

# ADMIN_ID опционален
_admin_raw = os.getenv("ADMIN_ID", "0")
try:
    ADMIN_ID = int(_admin_raw)
except ValueError:
    ADMIN_ID = 0

# Триала больше нет
def is_trial_active() -> bool:
    return True
