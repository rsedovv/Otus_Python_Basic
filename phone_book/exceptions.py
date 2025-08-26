class ValidationError(Exception):
    """Ошибка валидации данных контакта"""
    pass

class FileOperationError(Exception):
    """Ошибка работы с файлом"""
    pass

class ContactNotFoundError(Exception):
    """Контакт не найден"""
    pass