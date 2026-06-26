import os

DEFAULT_SKIP_EXTENSIONS = {".tmp", ".log", ".sys", ".md"}


def is_allowed(file_name, skip_extensions=DEFAULT_SKIP_EXTENSIONS):
    extension = os.path.splitext(file_name)[1].lower()

    if extension in skip_extensions:
        return False

    return True