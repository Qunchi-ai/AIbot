import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

START_DATE = datetime.strptime(os.getenv("START_DATE"), "%Y-%m-%d")
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "3"))

def is_trial_active():
    return datetime.now() < START_DATE + timedelta(days=TRIAL_DAYS)
