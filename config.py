# config.py

import os

# Ищем токен строго по переменной BOT_TOKEN (как в Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Добавьте его в переменные Railway.")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID не найден. Добавьте его в переменные Railway.")
