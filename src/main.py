import db_sqlite3
import scanner
import filter
import hasher
import os
import backup
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для сканирования папки, поиска дубликатов и сравнения с резервной копией."
    )

    # Добавляем обязательные аргументы (позиционные)
    parser.add_argument("folder_path", help="Путь к исходной папке для сканирования.")
    parser.add_argument("backup_folder", help="Путь к папке с резервной копией.")

    # Добавляем необязательный аргумент (флаг) для демонстрации операций с БД
    parser.add_argument("--demo-db", action="store_true",
                        help="Выполнить демонстрацию базовых операций с базой данных.")

    # Расширения для пропуска при сканировании
    parser.add_argument(
        "--skip-ext",
        nargs="*",
        default=[".tmp", ".log", ".sys", ".md"],
        help="Расширения файлов для пропуска, например: --skip-ext .tmp .log .sys"
    )

    args = parser.parse_args()  # Парсим переданные аргументы

    print(f"Папка для сканирования: {args.folder_path}")
    print(f"Папка с резервной копией: {args.backup_folder}")

    # Инициализируем базу данных
    db_sqlite3.init_db()

    db_sqlite3.demo_db()
    print("\nЭтап 1 завершён.")

    # Сканируем папку
    all_files = scanner.scan_folder(args.folder_path)

    # Фильтруем — оставляем только разрешённые файлы
    skip_extensions = set(args.skip_ext)
    allowed_files = [f for f in all_files if filter.is_allowed(f["path"], skip_extensions)]

    # Выводим список найденных файлов
    print(f"\nНайдено файлов: {len(allowed_files)}")
    for file in allowed_files:
        print(f"  {file['path']} | Размер: {file['size']} байт | Изменен: {file['modified_at']}")

    # Сохраняем результаты в базу данных
    db_sqlite3.save_files(allowed_files)
    db_sqlite3.save_scan_run(args.folder_path, len(allowed_files))
    print("\nЭтап 2 завершён.")

    # Считаем хэши и сохраняем в базу
    print("\nПодсчёт хэшей...")
    for file in allowed_files:
        full_path = os.path.join(args.folder_path, file["path"])
        file_hash = hasher.get_hash(full_path)
        db_sqlite3.save_hash(file["path"], file_hash)
        print(f"  {file['path']} -> {file_hash}")

    # Получаем из базы словарь дубликатов
    duplicates = db_sqlite3.get_duplicates()

    print("\nДубликаты:")
    if not duplicates:
        print("Дубликатов не найдено")
    else:
        for file_hash, paths in duplicates.items():
            print(f"\nХэш: {file_hash}")
            for path in paths:
                print(f"  {path}")

    print("\nЭтап 3 завершён.")

    # Инициализируем таблицу для хранения результатов сравнения бэкапов
    db_sqlite3.init_backup_table()

    # Сравниваем исходную папку с бэкапом
    result = backup.compare_folders(args.folder_path, args.backup_folder)

    # Выводим итоговый отчёт
    print(f"\nОтсутствуют в бэкапе ({len(result['missing'])}):")
    for path in result["missing"]:
        print(f"  {path}") if result["missing"] else print("  нет")

    print(f"\nЛишние в бэкапе ({len(result['extra'])}):")
    for path in result["extra"]:
        print(f"  {path}") if result["extra"] else print("  нет")

    print(f"\nИзменённые файлы ({len(result['changed'])}):")
    for path in result["changed"]:
        print(f"  {path}") if result["changed"] else print("  нет")

    # Сохраняем результат проверки в базу
    db_sqlite3.save_backup_check(args.folder_path, args.backup_folder, result)

    print("\nЭтап 4 завершён.")

    # Печать содержимого таблиц для наглядности
    db_sqlite3.print_table("files")
    db_sqlite3.print_table("scan_runs")
    db_sqlite3.print_table("backup_checks")


if __name__ == "__main__":
    main()