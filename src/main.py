import db_sqlite3
import scanner
import filter


def main():
    # Папка для сканирования — меняй на свою
    folder_path = r"C:\Users\User\Desktop"

    print(f"Папка: {folder_path}")

    # Инициализируем базу данных
    db_sqlite3.init_db()

    # # Демонстрация базовых операций
    # db_sqlite3.demo_db()
    #
    # print("Конец 1го этапа")

    # Сканируем папку
    all_files = scanner.scan_folder(folder_path)

    # Фильтруем — оставляем только разрешённые файлы
    allowed_files = [f for f in all_files if filter.is_allowed(f["path"])]

    # Выводим список найденных файлов
    print(f"\nНайдено файлов: {len(allowed_files)}")
    for file in allowed_files:
        print(f"  {file['path']}  {file['size']} байт  {file['modified_at']}")

    # Сохраняем результаты в базу данных
    db_sqlite3.save_files(allowed_files)
    db_sqlite3.save_scan_run(folder_path, len(allowed_files))
    db_sqlite3.print_all_files()
    print("\nЭтап 2 завершён.")

main()