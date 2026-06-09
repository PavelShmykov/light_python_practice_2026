import hashlib


def get_hash(full_path):
    # Создаём объект md5 для подсчёта хэша
    hasher = hashlib.md5()

    # Читаем файл кусками по 8192 байта
    # Чтобы не загружать большие файлы целиком в память
    with open(full_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(8192)

    # Возвращаем хэш в виде строки
    return hasher.hexdigest()
