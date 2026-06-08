import sqlite3
import os
import datetime


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

def demo_db():
    # Подсоединяемся к файлу БД
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    # Вставляем тестовую строку в таблицу files
    cursor.execute("""
        INSERT OR IGNORE INTO files (path, size, modified_at, extension, status)
        VALUES ('test/hello.txt', 1024, '2026-06-01 12:00:00', '.txt', 'active')
    """)

    conn.commit()
    print("INSERT: добавлена запись test/hello.txt")

    # Читаем все строки из таблицы files
    cursor.execute("SELECT id, path, size, status FROM files")

    for row in cursor.fetchall():
        print(f"SELECT: id={row[0]}  path={row[1]}  size={row[2]}  status={row[3]}")

    # Меняем поле status у конкретного файла
    cursor.execute(
        "UPDATE files SET status = 'missing' WHERE path = ?",
        ("test/hello.txt",)
    )
    conn.commit()
    print("UPDATE: статус изменён на missing")

    # SELECT после UPDATE — проверяем что изменение сохранилось
    cursor.execute("SELECT id, path, status FROM files")
    for row in cursor.fetchall():
        print(f"SELECT: id={row[0]}  path={row[1]}  status={row[2]}")

    # Удаляем строку где path совпадает с указанным значением
    cursor.execute("DELETE FROM files WHERE path = ?", ("test/hello.txt",))
    conn.commit()
    print("DELETE: запись удалена")

    conn.close()

def save_files(files):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Помечаем все существующие записи как отсутствующие
    # После сканирования обновим только найденные файлы
    cursor.execute("UPDATE files SET status = 'missing'")

    for file in files:
        # Если файл уже есть в базе — обновляем данные
        # Если нет — добавляем новую запись
        cursor.execute("""
            INSERT INTO files (path, size, modified_at, extension, status)
            VALUES (?, ?, ?, ?, 'active')
            ON CONFLICT(path) DO UPDATE SET
                size        = excluded.size,
                modified_at = excluded.modified_at,
                extension   = excluded.extension,
                status      = 'active'
        """, (file["path"], file["size"], file["modified_at"], file["extension"]))

    conn.commit()
    conn.close()

def save_scan_run(folder_path, files_count):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Записываем факт запуска сканирования
    scanned_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO scan_runs (folder, scanned_at) VALUES (?, ?)",
        (folder_path, scanned_at)
    )

    conn.commit()
    conn.close()
    print(f"Запуск сохранён: {folder_path} — {files_count} файлов — {scanned_at}")
