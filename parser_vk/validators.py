import re
from database import admin_tools
from hash_function import hash_word
from parser_vk.parser_vk_function import get_posts_vk
from loguru import logger

db = admin_tools.Admin()


# Функций валидаций введённых данных
def check_new_password(password: str, admin_id: str) -> str or list:
    """
    :param admin_id: Айди администратора
    :param password: Переданный пароль от пользователя
    :return: возвращаем результат проверки
    """
    if len(password) < 8:
        return "Простите, но ваш пароль короткий"

    elif re.search("[0-9]", password) is None:
        return "Проверьте, что в пароле содержатся цифры и повторите попытку"

    elif re.search("[A-Z]", password) is None:
        return "Убедитесь, что в вашем пароле есть заглавные буквы и повторите попытку"

    elif password is None:
        return ""

    elif len(password.split()) != 1:
        return "Извините, пароль не должен содержать пробелов"

    else:
        db.add_admins_to_database(user_id=admin_id)
        db.add_password_admin_to_base(admin_id=admin_id, password=hash_word(password))
        return [0, "Ваш пароль прошёл проверку и был внесён в базу данных"]


def check_correct_news(news: str) -> True | False:
    """
    :param news: Название мероприятия или группы вк
    :return: Возвращаем результат проверки
    """
    return bool(re.search('[а-яА-Я]', news))


def check_correct_hash(hash: str) -> True | False:
    """
    :param hash: Хэштег, введённый администратором
    :return: Возвращаем результат проверки правильности ввода хэштега
    """
    if answer := get_posts_vk(owner_id=hash, count=1)['items'][0]['text'] is not None:
        logger.debug(f'Ответ запроса {answer}')
        return True
    else:
        return False
