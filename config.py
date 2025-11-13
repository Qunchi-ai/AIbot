import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Локально подтягиваем .env, на Railway он просто не помешает
load_dotenv()

# --- ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ ---

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Не встановлено BOT_TOKEN в змінних середовища.")

# ADMIN_ID можно не ставити, тоді просто не буде відправки адміну
_admin_raw = os.getenv("ADMIN_ID", "0")
try:
    ADMIN_ID = int(_admin_raw)
except ValueError:
    ADMIN_ID = 0


# --- НАЛАШТУВАННЯ ТРІАЛУ ---

# Пытаемся прочитать START_DATE, но если его нет или он кривой —
# считаем, что триал стартует СЕЙЧАС, чтобы бот не падал.
_raw_start_date = os.getenv("START_DATE")

def _parse_start_date(raw: str | None) -> datetime:
    if not raw:
        # Бэкап: если переменной нет — стартуем триал с поточного моменту
        return datetime.utcnow()
    try:
        return datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        # Если формат кривой — тоже стартуем с сейчас
        return datetime.utcnow()

START_DATE = _parse_start_date(_raw_start_date)

# Кол-во дней триала
_raw_trial_days = os.getenv("TRIAL_DAYS", "3")
try:
    TRIAL_DAYS = int(_raw_trial_days)
except ValueError:
    TRIAL_DAYS = 3


def is_trial_active() -> bool:
    """
    Повертає True, якщо тріал ще активний.
    Працює навіть якщо змінні середовища були відсутні або криві.
    """
    now = datetime.utcnow()
    return now < START_DATE + timedelta(days=TRIAL_DAYS)
