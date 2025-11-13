import sqlite3
from datetime import datetime

DB_NAME = "leads.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        answers TEXT,
        status TEXT DEFAULT 'new',
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

def save_lead(user_id, name, phone, answers):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO leads (user_id, name, phone, answers, created_at) VALUES (?,?,?,?,?)',
              (user_id, name, phone, str(answers), datetime.now().isoformat()))
    conn.commit()
    conn.close()
