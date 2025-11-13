import sqlite3

def save_lead(user_id: int, name: str, phone: str, answers: list[str]):
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        q1 TEXT,
        q2 TEXT,
        q3 TEXT
    )
    """)

    c.execute("""
    INSERT INTO leads (user_id, name, phone, q1, q2, q3)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, name, phone, answers[0], answers[1], answers[2]))

    conn.commit()
    conn.close()
