import sqlite3

def init_db():
    conn = sqlite3.connect("mistakes.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            correction TEXT,
            explanation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_mistake(user_input, correction, explanation):
    conn = sqlite3.connect("mistakes.db")
    c = conn.cursor()
    c.execute("INSERT INTO mistakes (user_input, correction, explanation) VALUES (?, ?, ?)",
              (user_input, correction, explanation))
    conn.commit()
    conn.close()

def get_all_mistakes():
    conn = sqlite3.connect("mistakes.db")
    c = conn.cursor()
    c.execute("SELECT user_input, correction, explanation FROM mistakes")
    data = c.fetchall()
    conn.close()
    return data
