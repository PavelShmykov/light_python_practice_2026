import sqlite3
import os


DB_PATH = "data/app.db"


def init_db():
    # Создаём папку data/ если её нет
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица индекса файлов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            path        TEXT NOT NULL UNIQUE,
            size        INTEGER,
            modified_at TEXT,
            extension   TEXT,
            status      TEXT DEFAULT 'active'
        )
    """)

    # Таблица истории запусков
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_runs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            folder     TEXT NOT NULL,
            scanned_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"База данных создана: {DB_PATH}")
