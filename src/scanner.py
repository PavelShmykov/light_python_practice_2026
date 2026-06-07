import os
import datetime


def scan_folder(folder_path):
    # Список куда складываем информацию о каждом файле
    files = []

    # Запускаем рекурсивный обход с корневой папки
    scan_recursive(folder_path, folder_path, files)

    return files


def scan_recursive(current_folder, root_folder, files):
    # Получаем список всего содержимого текущей папки
    entries = os.listdir(current_folder)

    for entry in entries:
        # Полный путь к текущему элементу
        full_path = os.path.join(current_folder, entry)

        if os.path.isdir(full_path):
            # Если это папка — заходим в неё рекурсивно
            scan_recursive(full_path, root_folder, files)

        elif os.path.isfile(full_path):
            # Если это файл — собираем данные о нём

            # Относительный путь от корневой папки
            relative_path = os.path.relpath(full_path, root_folder)

            # Размер файла в байтах
            size = os.path.getsize(full_path)

            # Дата последнего изменения
            modified_timestamp = os.path.getmtime(full_path)
            modified_at = datetime.datetime.fromtimestamp(modified_timestamp)
            modified_at = modified_at.strftime("%Y-%m-%d %H:%M:%S")

            # Расширение файла
            extension = os.path.splitext(entry)[1].lower()

            # Добавляем файл в список
            files.append({
                "path": relative_path,
                "size": size,
                "modified_at": modified_at,
                "extension": extension,
            })
