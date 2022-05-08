import re
from database import admin_tools
from hash_function import hash_word

db = admin_tools.Admin()


# Функций валидаций введённых данных
def check_new_password(password, admin_id):
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

    else:
        db.add_admins_to_database(user_id=admin_id)
        db.add_password_admin_to_base(admin_id=admin_id, password=hash_word(password))
        return [0, "Ваш пароль прошёл проверку и был внесён в базу данных"]
