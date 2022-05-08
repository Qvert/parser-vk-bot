import hashlib


def hash_word(word_str: str) -> str:
    """
    :param word_str: Пароль или данные для хэширования
    :return: Ыозвращаем хэшированную строку
    """
    # uuid используется для генерации случайного числа

    return str(hashlib.sha256(word_str.encode()).hexdigest())


def check_word(hashed_password: str, user_password: str) -> True | False:
    """
    :param hashed_password: Захэшированный пароль
    :param user_password: Незахэшированный пароль для проверки
    :return:
    """
    return hashed_password == str(hashlib.sha256(user_password.encode()).hexdigest())

