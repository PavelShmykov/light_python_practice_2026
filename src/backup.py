import os
import scanner


def compare_folders(source_folder, backup_folder):
    # Сканируем исходную папку
    source_files_list = []
    scanner.scan_recursive(source_folder, source_folder, source_files_list)

    # Сканируем папку с бэкапом
    backup_files_list = []
    scanner.scan_recursive(backup_folder, backup_folder, backup_files_list)

    # Преобразуем списки в словари: путь -> размер
    # Так удобно искать файл по пути и сравнивать размеры
    source_files = {f["path"]: f["size"] for f in source_files_list}
    backup_files = {f["path"]: f["size"] for f in backup_files_list}

    # Файлы которые есть в source но нет в backup
    missing = sorted([p for p in source_files if p not in backup_files])

    # Файлы которые есть в backup но нет в source
    extra = sorted([p for p in backup_files if p not in source_files])

    # Файлы которые есть в обоих — но размер отличается
    changed = sorted([
        p for p in source_files
        if p in backup_files and source_files[p] != backup_files[p]
    ])

    return {
        "missing": missing,
        "extra": extra,
        "changed": changed,
    }
