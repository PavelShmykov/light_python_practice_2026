import os


# Расширения которые пропускаем при сканировании
SKIP_EXTENSIONS = {".tmp", ".log", ".sys"}


def is_allowed(file_name):
    # Получаем расширение файла в нижнем регистре
    extension = os.path.splitext(file_name)[1].lower()

    # Возвращаем False если расширение в списке запрещённых
    if extension in SKIP_EXTENSIONS:
        return False

    return True
