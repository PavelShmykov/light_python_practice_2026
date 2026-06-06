import db_sqlite3


def main():
    # Папка для сканирования — меняй на свою
    folder_path = r"C:\Users\User\Desktop"

    print(f"Папка: {folder_path}")

    # Инициализируем базу данных
    db_sqlite3.init_db()

    # Демонстрация базовых операций
    db_sqlite3.demo_db()

    print("Конец 1го этапа")


main()