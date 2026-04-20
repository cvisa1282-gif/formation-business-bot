import sqlite3
from datetime import datetime

# ====================== DATABASE ======================
def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            credits INTEGER DEFAULT 0,
            referrer_id INTEGER,
            join_date TEXT,
            banned INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY,
            referrer_id INTEGER,
            referred_id INTEGER,
            date TEXT
        );

        CREATE TABLE IF NOT EXISTS formations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price INTEGER,
            file_id TEXT,
            added_date TEXT
        );

        CREATE TABLE IF NOT EXISTS pending_payments (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            credits INTEGER,
            cfa INTEGER,
            screenshot TEXT,
            date TEXT
        );

        CREATE TABLE IF NOT EXISTS pending_withdrawals (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount_cfa INTEGER,
            method TEXT,
            phone TEXT,
            country TEXT,
            date TEXT
        );
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée")

def add_credits(user_id: int, amount: int):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return c.fetchone()

print("✅ database.py chargé avec succès OK")
