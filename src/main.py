import db_sqlite3
import scanner
import filter
import hasher
import os
import backup


def main():
    # Папка для сканирования — меняй на свою
    folder_path = r"C:\Users\User\light_python_practice_2026\src\test_folder"

    # Папка с резервной копией — меняй на свою
    backup_folder = r"C:\Users\User\light_python_practice_2026\src\backup_folder"

    print(f"Папка: {folder_path}")

    # Инициализируем базу данных
    db_sqlite3.init_db()

    # Демонстрация базовых операций
    db_sqlite3.demo_db()

    print("\nЭтап 1 завершён.")

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
    print("\nЭтап 2 завершён.")

    # Добавляем колонку hash если её нет
    # db_sqlite3.add_hash_column()

    # Сканируем папку
    all_files = scanner.scan_folder(folder_path)

    # Фильтруем — оставляем только разрешённые файлы
    allowed_files = [f for f in all_files if filter.is_allowed(f["path"])]

    # Выводим список найденных файлов
    print(f"\nНайдено файлов: {len(allowed_files)}")
    for file in allowed_files:
        print(f"{file['path']}  {file['size']} байт  {file['modified_at']}")

    # Сохраняем результаты в базу данных
    db_sqlite3.save_files(allowed_files)
    db_sqlite3.save_scan_run(folder_path, len(allowed_files))

    # Считаем хэши и сохраняем в базу
    print("\nПодсчёт хэшей...")
    for file in allowed_files:
        # Собираем полный путь к файлу на диске
        # folder_path + относительный путь = полный путь
        # Например: C:\Desktop + foto\image.jpg = C:\Desktop\foto\image.jpg
        full_path = os.path.join(folder_path, file["path"])

        # Считаем хэш содержимого файла
        file_hash = hasher.get_hash(full_path)

        # Сохраняем хэш в базу данных для этого файла
        db_sqlite3.save_hash(file["path"], file_hash)

        # Выводим путь и хэш в консоль
        print(f"  {file['path']}  {file_hash}")

    # Получаем из базы словарь дубликатов
    duplicates = db_sqlite3.get_duplicates()

    print("\nДубликаты")

    if not duplicates:
        # Словарь пустой — дубликатов нет
        print("Дубликатов не найдено")
    else:
        # Перебираем каждую группу дубликатов
        for file_hash, paths in duplicates.items():
            # Выводим хэш группы
            print(f"\nХэш: {file_hash}")

            # Выводим все файлы с этим хэшем
            for path in paths:
                print(f"  {path}")

    print("\nЭтап 3 завершён.")

    # Инициализируем таблицу для хранения результатов
    db_sqlite3.init_backup_table()

    # Сравниваем исходную папку с бэкапом
    result = backup.compare_folders(folder_path, backup_folder)

    # Выводим итоговый отчёт
    print(f"\nОтсутствуют в бэкапе ({len(result['missing'])}):")
    if result["missing"]:
        for path in result["missing"]:
            print(f"  {path}")
    else:
        print("  нет")

    print(f"\nЛишние в бэкапе ({len(result['extra'])}):")
    if result["extra"]:
        for path in result["extra"]:
            print(f"  {path}")
    else:
        print("  нет")

    print(f"\nИзменённые файлы ({len(result['changed'])}):")
    if result["changed"]:
        for path in result["changed"]:
            print(f"  {path}")
    else:
        print("  нет")

    # Сохраняем результат проверки в базу
    db_sqlite3.save_backup_check(folder_path, backup_folder, result)

    print("\nЭтап 4 завершён.")

    # db_sqlite3.print_table("files")
    # db_sqlite3.print_table("scan_runs")
    # db_sqlite3.print_table("backup_checks")

main()
